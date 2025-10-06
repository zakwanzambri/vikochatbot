"""
Intelligent Document-Based Chatbot
Answers questions based on uploaded documents (PDF, DOCX, TXT)
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
from typing import List, Optional
import shutil

# Document processing imports
from PyPDF2 import PdfReader
from docx import Document

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


class DocumentProcessor:
    """Handles document text extraction and cleaning"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PdfReader(file_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text(file_path: str, file_extension: str) -> str:
        """Extract text based on file type"""
        if file_extension == '.pdf':
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return DocumentProcessor.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return DocumentProcessor.extract_text_from_txt(file_path)
        else:
            return ""


class VectorStoreManager:
    """Manages vector store operations with FAISS"""
    
    def __init__(self, openai_api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def create_vector_store(self, texts: List[str]) -> Optional[FAISS]:
        """Create FAISS vector store from texts"""
        try:
            if not texts or not any(texts):
                return None
            
            # Split texts into chunks
            chunks = []
            for text in texts:
                if text:
                    chunks.extend(self.text_splitter.split_text(text))
            
            if not chunks:
                return None
            
            # Create vector store
            vector_store = FAISS.from_texts(chunks, self.embeddings)
            return vector_store
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")
            return None


class ChatbotEngine:
    """Main chatbot engine using RAG"""
    
    def __init__(self, vector_store: FAISS, openai_api_key: str):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=openai_api_key
        )
        
        # Create conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )
    
    def get_answer(self, question: str) -> str:
        """Get answer for a question based on documents"""
        try:
            response = self.chain({"question": question})
            answer = response.get("answer", "")
            
            # Check if the answer indicates information was not found
            if not answer or len(answer.strip()) < 10:
                return "I couldn't find that info in the uploaded documents."
            
            # Check for common phrases indicating uncertainty
            uncertainty_phrases = [
                "i don't know",
                "not mentioned",
                "no information",
                "cannot find",
                "not found",
                "doesn't say",
                "not provided"
            ]
            
            if any(phrase in answer.lower() for phrase in uncertainty_phrases):
                return "I couldn't find that info in the uploaded documents."
            
            return answer
        except Exception as e:
            st.error(f"Error getting answer: {str(e)}")
            return "I couldn't find that info in the uploaded documents."


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Viko Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Viko Chatbot - Document-Based Q&A")
    st.markdown("Upload your documents (PDF, DOCX, TXT) and ask questions about them!")
    
    initialize_session_state()
    
    # Sidebar for API key and document upload
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # OpenAI API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key"
        )
        
        st.divider()
        
        st.header("📁 Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload PDF, DOCX, or TXT files"
        )
        
        process_button = st.button("🔄 Process Documents", use_container_width=True)
        
        if process_button and uploaded_files and api_key:
            with st.spinner("Processing documents..."):
                # Extract text from all uploaded files
                all_texts = []
                processed_files = []
                
                for uploaded_file in uploaded_files:
                    # Save file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    
                    # Extract text
                    file_extension = Path(uploaded_file.name).suffix.lower()
                    text = DocumentProcessor.extract_text(tmp_path, file_extension)
                    
                    if text:
                        all_texts.append(text)
                        processed_files.append(uploaded_file.name)
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                
                if all_texts:
                    # Create vector store
                    vector_store_manager = VectorStoreManager(api_key)
                    vector_store = vector_store_manager.create_vector_store(all_texts)
                    
                    if vector_store:
                        # Create chatbot
                        st.session_state.vector_store = vector_store
                        st.session_state.chatbot = ChatbotEngine(vector_store, api_key)
                        st.session_state.documents_processed = True
                        st.session_state.chat_history = []
                        
                        st.success(f"✅ Processed {len(processed_files)} document(s)!")
                        st.info("📄 Files: " + ", ".join(processed_files))
                    else:
                        st.error("Failed to create vector store")
                else:
                    st.error("No text could be extracted from the uploaded files")
        
        elif process_button and not api_key:
            st.error("Please enter your OpenAI API key")
        elif process_button and not uploaded_files:
            st.error("Please upload at least one document")
    
    # Main chat interface
    if st.session_state.documents_processed and st.session_state.chatbot:
        st.success("✅ Documents processed! Ask me anything about your documents.")
        
        # Display chat history
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(question)
            with st.chat_message("assistant"):
                st.write(answer)
        
        # Chat input
        user_question = st.chat_input("Ask a question about your documents...")
        
        if user_question:
            # Add user message to chat
            with st.chat_message("user"):
                st.write(user_question)
            
            # Get answer from chatbot
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = st.session_state.chatbot.get_answer(user_question)
                    st.write(answer)
            
            # Save to chat history
            st.session_state.chat_history.append((user_question, answer))
    else:
        st.info("👈 Please upload documents and process them to start chatting!")
        
        # Display instructions
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. **Enter your OpenAI API Key** in the sidebar
            2. **Upload documents** (PDF, DOCX, or TXT files)
            3. **Click 'Process Documents'** to analyze your files
            4. **Ask questions** about your documents in the chat
            
            The chatbot will answer based only on the content of your uploaded documents.
            If the information is not found, it will let you know!
            """)


if __name__ == "__main__":
    main()
