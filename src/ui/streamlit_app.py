"""
Streamlit Web Interface for Document Chatbot
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.document_processor import PDFExtractor, DOCXExtractor, TextExtractor
from src.embedding import TextChunker, OpenAIEmbedder
from src.vector_store import FAISSVectorStore, ChromaVectorStore
from src.retrieval import DocumentRetriever
from src.llm import ChatBot
from src.config import (
    UPLOADS_DIR, VECTOR_DB_DIR, CHUNK_SIZE, CHUNK_OVERLAP,
    VECTOR_STORE_TYPE, COLLECTION_NAME, OPENAI_API_KEY, ERROR_NO_API_KEY
)
import os
import shutil


# Page configuration
st.set_page_config(
    page_title="📚 Document Q&A Chatbot",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .source-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        background-color: #e1f5ff;
        border-radius: 1rem;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'retriever' not in st.session_state:
        st.session_state.retriever = None
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []


def process_document(file, file_path: str):
    """Process a single document and return extracted data"""
    file_ext = Path(file.name).suffix.lower()
    
    try:
        if file_ext == '.pdf':
            extractor = PDFExtractor()
        elif file_ext == '.docx':
            extractor = DOCXExtractor()
        elif file_ext == '.txt':
            extractor = TextExtractor()
        else:
            return None, f"Unsupported file type: {file_ext}"
        
        data = extractor.extract_text(file_path)
        return data, None
    except Exception as e:
        return None, str(e)


def load_or_create_vector_store():
    """Load existing or create new vector store"""
    try:
        if VECTOR_STORE_TYPE == "faiss":
            index_path = VECTOR_DB_DIR / "faiss_index"
            vector_store = FAISSVectorStore(index_path=str(index_path))
            
            # Try to load existing index
            if (Path(str(index_path) + ".index")).exists():
                vector_store.load()
                return vector_store, True
            return vector_store, False
            
        else:  # chroma
            vector_store = ChromaVectorStore(
                collection_name=COLLECTION_NAME,
                persist_directory=str(VECTOR_DB_DIR / "chroma")
            )
            stats = vector_store.get_stats()
            return vector_store, stats['total_documents'] > 0
            
    except Exception as e:
        st.error(f"Error loading vector store: {str(e)}")
        return None, False


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">📚 Document Q&A Chatbot</div>', unsafe_allow_html=True)
    st.markdown("Upload your documents (PDF, DOCX, TXT) and ask questions about their content!")
    
    # Check API key
    if not OPENAI_API_KEY:
        st.error(ERROR_NO_API_KEY)
        st.info("Please create a `.env` file in the project root and add your OpenAI API key.")
        st.code("OPENAI_API_KEY=your_api_key_here")
        return
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("📁 Document Upload")
        
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload PDF, DOCX, or TXT files"
        )
        
        if st.button("🔄 Process Documents", type="primary"):
            if not uploaded_files:
                st.warning("Please upload at least one document.")
            else:
                process_documents(uploaded_files)
        
        st.divider()
        
        # Load existing documents
        if st.button("📂 Load Existing Database"):
            load_existing_database()
        
        # Clear database
        if st.button("🗑️ Clear Database", type="secondary"):
            clear_database()
        
        st.divider()
        
        # Statistics
        if st.session_state.vector_store:
            st.subheader("📊 Statistics")
            stats = st.session_state.vector_store.get_stats()
            
            if VECTOR_STORE_TYPE == "faiss":
                st.metric("Total Chunks", stats['total_vectors'])
            else:
                st.metric("Total Chunks", stats['total_documents'])
            
            if st.session_state.processed_files:
                st.write("**Processed Files:**")
                for f in st.session_state.processed_files:
                    st.write(f"• {f}")
    
    # Main chat interface
    st.header("💬 Ask Questions")
    
    if not st.session_state.documents_loaded:
        st.info("👈 Upload and process documents from the sidebar to start chatting!")
    else:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    st.markdown("**📎 Sources:**")
                    sources_html = "".join([f'<span class="source-badge">{s}</span>' for s in message["sources"]])
                    st.markdown(sources_html, unsafe_allow_html=True)
        
        # Chat input
        if question := st.chat_input("Ask a question about your documents..."):
            # Add user message to chat
            st.session_state.chat_history.append({"role": "user", "content": question})
            
            with st.chat_message("user"):
                st.markdown(question)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        result = st.session_state.chatbot.chat_with_retrieval(
                            question,
                            st.session_state.retriever,
                            top_k=5
                        )
                        
                        answer = result['answer']
                        sources = result['sources']
                        
                        st.markdown(answer)
                        
                        if sources:
                            st.markdown("**📎 Sources:**")
                            sources_html = "".join([f'<span class="source-badge">{s}</span>' for s in sources])
                            st.markdown(sources_html, unsafe_allow_html=True)
                        
                        # Add to history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": error_msg
                        })
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()


def process_documents(uploaded_files):
    """Process uploaded documents"""
    with st.spinner("Processing documents..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        all_chunks = []
        processed_count = 0
        error_count = 0
        
        # Initialize components
        try:
            embedder = OpenAIEmbedder()
            chunker = TextChunker(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
            vector_store, _ = load_or_create_vector_store()
            
            if not vector_store:
                st.error("Failed to initialize vector store")
                return
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing: {uploaded_file.name}")
                
                # Save uploaded file
                file_path = UPLOADS_DIR / uploaded_file.name
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                # Extract text
                data, error = process_document(uploaded_file, str(file_path))
                
                if error:
                    st.warning(f"Error processing {uploaded_file.name}: {error}")
                    error_count += 1
                    continue
                
                # Chunk text
                chunks = chunker.chunk_text(
                    data['text'],
                    metadata={'filename': uploaded_file.name, 'file_type': data.get('file_type', 'unknown')}
                )
                
                # Generate embeddings
                chunks_with_embeddings = embedder.embed_chunks(chunks)
                all_chunks.extend(chunks_with_embeddings)
                
                processed_count += 1
                st.session_state.processed_files.append(uploaded_file.name)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            # Add to vector store
            if all_chunks:
                status_text.text("Adding to vector store...")
                vector_store.add_documents(all_chunks)
                
                # Save vector store
                if VECTOR_STORE_TYPE == "faiss":
                    vector_store.save()
                else:
                    vector_store.save()
                
                # Initialize retriever and chatbot
                st.session_state.vector_store = vector_store
                st.session_state.retriever = DocumentRetriever(vector_store, embedder)
                st.session_state.chatbot = ChatBot()
                st.session_state.documents_loaded = True
                
                progress_bar.progress(1.0)
                status_text.text("✅ Processing complete!")
                
                st.success(f"Successfully processed {processed_count} documents with {len(all_chunks)} chunks!")
                if error_count > 0:
                    st.warning(f"{error_count} documents had errors.")
            else:
                st.error("No valid text extracted from documents.")
                
        except Exception as e:
            st.error(f"Error during processing: {str(e)}")


def load_existing_database():
    """Load existing vector database"""
    try:
        vector_store, has_data = load_or_create_vector_store()
        
        if has_data:
            embedder = OpenAIEmbedder()
            st.session_state.vector_store = vector_store
            st.session_state.retriever = DocumentRetriever(vector_store, embedder)
            st.session_state.chatbot = ChatBot()
            st.session_state.documents_loaded = True
            
            stats = vector_store.get_stats()
            st.success(f"✅ Loaded existing database with {stats.get('total_vectors', stats.get('total_documents', 0))} chunks!")
        else:
            st.info("No existing database found. Please upload documents.")
            
    except Exception as e:
        st.error(f"Error loading database: {str(e)}")


def clear_database():
    """Clear all data"""
    try:
        # Clear vector store
        if st.session_state.vector_store:
            st.session_state.vector_store.clear()
            
            # Delete files
            if VECTOR_STORE_TYPE == "faiss":
                index_path = VECTOR_DB_DIR / "faiss_index"
                for ext in ['.index', '.pkl']:
                    file_path = Path(str(index_path) + ext)
                    if file_path.exists():
                        file_path.unlink()
        
        # Clear uploads
        if UPLOADS_DIR.exists():
            for file in UPLOADS_DIR.iterdir():
                if file.is_file():
                    file.unlink()
        
        # Reset session state
        st.session_state.vector_store = None
        st.session_state.retriever = None
        st.session_state.chatbot = None
        st.session_state.documents_loaded = False
        st.session_state.chat_history = []
        st.session_state.processed_files = []
        
        st.success("✅ Database cleared!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error clearing database: {str(e)}")


if __name__ == "__main__":
    main()
