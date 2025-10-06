"""
LLM Chat Completion using OpenAI
"""
from openai import OpenAI
from typing import List, Dict
from src.config import OPENAI_API_KEY, CHAT_MODEL, ERROR_NO_CONTEXT


class ChatBot:
    """Chat completion with context from documents"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the chatbot
        
        Args:
            api_key: OpenAI API key (defaults to config)
            model: Chat model to use (defaults to config)
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or CHAT_MODEL
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # System prompt for RAG
        self.system_prompt = """You are a helpful AI assistant that answers questions based on provided documents.

IMPORTANT RULES:
1. Answer questions ONLY using information from the provided context/documents
2. If the answer is not in the documents, respond with: "⚠️ I couldn't find that information in your documents."
3. Always cite which source document you're using when answering
4. Be concise and accurate
5. If you're not completely sure, acknowledge the uncertainty
6. Do not make up information or use external knowledge

When you find relevant information, format your answer clearly and mention the source."""
    
    def chat(self, question: str, context: str = "", conversation_history: List[Dict] = None) -> str:
        """
        Generate a response to a question with optional context
        
        Args:
            question: User's question
            context: Retrieved document context
            conversation_history: Previous messages in the conversation
            
        Returns:
            Generated response
        """
        if not question or not question.strip():
            return "Please ask a question."
        
        # Build messages
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current question with context
        if context and context.strip():
            user_message = f"""Context from documents:
{context}

Question: {question}

Please answer based on the context above."""
        else:
            user_message = f"""No relevant context found in the documents.

Question: {question}

Since there is no context, please respond with: "{ERROR_NO_CONTEXT}" """
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"
    
    def chat_with_retrieval(self, question: str, retriever, top_k: int = 5) -> Dict:
        """
        Complete RAG pipeline: retrieve context and generate answer
        
        Args:
            question: User's question
            retriever: DocumentRetriever instance
            top_k: Number of chunks to retrieve
            
        Returns:
            Dictionary containing answer, sources, and retrieved chunks
        """
        # Retrieve relevant chunks
        retrieved_chunks = retriever.retrieve(question, top_k=top_k)
        
        # Format context
        context = retriever.format_context(retrieved_chunks)
        
        # Generate answer
        answer = self.chat(question, context)
        
        # Get sources
        sources = retriever.get_relevant_sources(retrieved_chunks)
        
        return {
            'answer': answer,
            'sources': sources,
            'retrieved_chunks': retrieved_chunks,
            'num_chunks': len(retrieved_chunks)
        }
    
    def chat_streaming(self, question: str, context: str = ""):
        """
        Generate a streaming response (generator)
        
        Args:
            question: User's question
            context: Retrieved document context
            
        Yields:
            Response chunks as they're generated
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if context and context.strip():
            user_message = f"""Context from documents:
{context}

Question: {question}

Please answer based on the context above."""
        else:
            user_message = f"Question: {question}\n\nNo relevant context found. {ERROR_NO_CONTEXT}"
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1000,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"❌ Error: {str(e)}"
