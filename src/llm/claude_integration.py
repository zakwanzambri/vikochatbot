"""
Anthropic Claude integration for chat
Note: Anthropic doesn't have embeddings, so use with OpenAI/Cohere embeddings
"""
from anthropic import Anthropic
from typing import List, Dict
import os


class ClaudeChat:
    """Chat completion using Anthropic's Claude"""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize Claude chat
        
        Args:
            api_key: Anthropic API key
            model: Model name (claude-3-5-sonnet, claude-3-opus, etc.)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        
        self.system_prompt = """You are a helpful AI assistant that answers questions based on provided documents.

IMPORTANT RULES:
1. Answer questions ONLY using information from the provided context/documents
2. If the answer is not in the documents, respond with: "⚠️ I couldn't find that information in your documents."
3. Always cite which source document you're using when answering
4. Be concise and accurate
5. If you're not completely sure, acknowledge the uncertainty
6. Do not make up information or use external knowledge

When you find relevant information, format your answer clearly and mention the source."""
    
    def chat(self, question: str, context: str = "") -> str:
        """Generate a response to a question with context"""
        
        if context:
            user_message = f"""Context from documents:
{context}

Question: {question}

Please answer based on the context above."""
        else:
            user_message = f"""Question: {question}

No relevant context found. Please respond with: "⚠️ I couldn't find that information in your documents." """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"❌ Error: {str(e)}"
