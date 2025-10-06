# 🔄 System Architecture & Data Flow

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (Streamlit)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Upload Files │  │  Chat Input  │  │   Database   │     │
│  │   (Sidebar)  │  │   (Main)     │  │  Management  │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                        │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            DOCUMENT PROCESSING PIPELINE              │  │
│  │                                                       │  │
│  │  1. Document Upload                                  │  │
│  │     ↓                                                │  │
│  │  2. Text Extraction (PDF/DOCX/TXT)                  │  │
│  │     ↓                                                │  │
│  │  3. Text Chunking (Smart Splitting)                 │  │
│  │     ↓                                                │  │
│  │  4. Embedding Generation (OpenAI)                   │  │
│  │     ↓                                                │  │
│  │  5. Vector Storage (FAISS/ChromaDB)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               QUERY PROCESSING PIPELINE              │  │
│  │                                                       │  │
│  │  1. User Question                                    │  │
│  │     ↓                                                │  │
│  │  2. Question Embedding (OpenAI)                     │  │
│  │     ↓                                                │  │
│  │  3. Semantic Search (Vector DB)                     │  │
│  │     ↓                                                │  │
│  │  4. Context Retrieval (Top-K Chunks)                │  │
│  │     ↓                                                │  │
│  │  5. LLM Generation (GPT-4 + Context)                │  │
│  │     ↓                                                │  │
│  │  6. Answer with Citations                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                           │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Uploads    │  │  Vector DB   │  │   Session    │      │
│  │   (Files)    │  │ (Embeddings) │  │    State     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                         │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              OpenAI API                               │  │
│  │  • text-embedding-3-small (Embeddings)               │  │
│  │  • gpt-4o / gpt-4-turbo (Chat Completion)           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Detailed Data Flow

### 📤 Document Upload Flow

```
User Action: Upload PDF/DOCX/TXT
    ↓
Save to: data/uploads/filename.ext
    ↓
┌─────────────────────────────────┐
│  Document Extraction            │
│  • PDFExtractor (PyMuPDF)      │
│  • DOCXExtractor (python-docx) │
│  • TextExtractor (chardet)     │
└─────────────┬───────────────────┘
              ↓
    Extracted Text String
              ↓
┌─────────────────────────────────┐
│  Text Chunking                  │
│  • Size: 1000 chars            │
│  • Overlap: 200 chars          │
│  • Smart boundaries            │
└─────────────┬───────────────────┘
              ↓
    List of Text Chunks
    [chunk1, chunk2, ...]
              ↓
┌─────────────────────────────────┐
│  Embedding Generation           │
│  • Model: text-embedding-3-small│
│  • Dimension: 1536             │
│  • Batch processing            │
└─────────────┬───────────────────┘
              ↓
    Chunks + Embeddings
    [{text, embedding, metadata}]
              ↓
┌─────────────────────────────────┐
│  Vector Storage                 │
│  • FAISS: IndexFlatL2          │
│  • ChromaDB: Persistent        │
│  • Metadata: filename, etc     │
└─────────────┬───────────────────┘
              ↓
    Stored in Vector Database
    ✅ Ready for Queries
```

### 💬 Question-Answer Flow

```
User Action: Type Question
    ↓
    "What is the main topic?"
    ↓
┌─────────────────────────────────┐
│  Query Embedding                │
│  • Convert to 1536-dim vector  │
│  • Same model as docs          │
└─────────────┬───────────────────┘
              ↓
    Query Vector [0.123, -0.456, ...]
              ↓
┌─────────────────────────────────┐
│  Similarity Search              │
│  • Compare with all doc chunks │
│  • Calculate cosine similarity │
│  • Rank by relevance           │
└─────────────┬───────────────────┘
              ↓
    Top-5 Most Similar Chunks
    [chunk1(0.92), chunk2(0.87), ...]
              ↓
┌─────────────────────────────────┐
│  Context Formatting             │
│  • Add source citations        │
│  • Format for LLM              │
│  • Limit token count           │
└─────────────┬───────────────────┘
              ↓
    Formatted Context String
    "[Source 1: doc.pdf]
     Content here..."
              ↓
┌─────────────────────────────────┐
│  LLM Completion                 │
│  • Model: GPT-4o               │
│  • Temperature: 0.3            │
│  • System: RAG instructions    │
│  • Input: Question + Context   │
└─────────────┬───────────────────┘
              ↓
    Generated Answer
    "Based on the documents..."
              ↓
┌─────────────────────────────────┐
│  Response Formatting            │
│  • Extract answer              │
│  • List sources                │
│  • Show relevance scores       │
└─────────────┬───────────────────┘
              ↓
    Display to User
    ✅ Answer + Sources + Scores
```

## 🧩 Component Interactions

### Document Processor ↔ Embedder
```python
# Extract text
extractor = PDFExtractor()
data = extractor.extract_text("doc.pdf")
text = data['text']

# Pass to chunker
chunker = TextChunker()
chunks = chunker.chunk_text(text, metadata={'filename': 'doc.pdf'})

# Generate embeddings
embedder = OpenAIEmbedder()
embedded_chunks = embedder.embed_chunks(chunks)
```

### Vector Store ↔ Retriever
```python
# Store embeddings
vector_store = FAISSVectorStore()
vector_store.add_documents(embedded_chunks)

# Later: Retrieve similar documents
retriever = DocumentRetriever(vector_store, embedder)
results = retriever.retrieve("user question")
```

### Retriever ↔ ChatBot
```python
# Retrieve context
retriever = DocumentRetriever(vector_store, embedder)
retrieved_chunks = retriever.retrieve(question, top_k=5)
context = retriever.format_context(retrieved_chunks)

# Generate answer
chatbot = ChatBot()
answer = chatbot.chat(question, context)
```

## 📊 Module Dependencies

```
streamlit_app.py
    ↓ imports
    ├─→ config.py (settings)
    ├─→ document_processor (extract text)
    │   ├─→ pdf_extractor.py
    │   ├─→ docx_extractor.py
    │   └─→ text_extractor.py
    ├─→ embedding (chunk & embed)
    │   ├─→ chunker.py
    │   └─→ embedder.py (→ OpenAI API)
    ├─→ vector_store (storage)
    │   ├─→ faiss_store.py (→ FAISS)
    │   └─→ chroma_store.py (→ ChromaDB)
    ├─→ retrieval (search)
    │   └─→ retriever.py
    └─→ llm (chat)
        └─→ chat_completion.py (→ OpenAI API)
```

## 🔐 API Call Flow

```
Application Start
    ↓
Load API Key from .env
    ↓
Initialize OpenAI Client
    ↓
┌─────────────────────────────────────┐
│         EMBEDDING CALLS             │
│  Document Processing:               │
│    • ~10-50 calls per document     │
│    • Batch processing (100/batch)  │
│    • Cost: ~$0.00002 per 1K tokens │
└─────────────┬───────────────────────┘
              ↓
    Store embeddings locally
    (No more API calls until new docs)
              ↓
┌─────────────────────────────────────┐
│           QUERY CALLS               │
│  Per Question:                      │
│    • 1 embedding call (question)   │
│    • 1 chat completion call        │
│    • Cost: ~$0.01-0.05 per Q       │
└─────────────────────────────────────┘
```

## 💾 Storage Organization

```
data/
├── uploads/                    # User uploaded files
│   ├── document1.pdf
│   ├── document2.docx
│   └── notes.txt
│
└── vector_db/                  # Vector database
    ├── faiss_index.index      # FAISS index file
    ├── faiss_index.pkl        # FAISS metadata
    │
    └── chroma/                # ChromaDB directory
        ├── chroma.sqlite3
        └── [collection files]
```

## 🔄 Session State (Streamlit)

```python
st.session_state = {
    'vector_store': FAISSVectorStore,      # Active vector DB
    'retriever': DocumentRetriever,        # Search engine
    'chatbot': ChatBot,                    # LLM interface
    'chat_history': [                      # Conversation
        {'role': 'user', 'content': '...'},
        {'role': 'assistant', 'content': '...', 'sources': [...]}
    ],
    'documents_loaded': True,              # Ready status
    'processed_files': ['doc1.pdf', ...]   # Uploaded files
}
```

## ⚡ Performance Characteristics

### Time Complexity
| Operation | Time | Notes |
|-----------|------|-------|
| PDF Extraction | O(n) | n = pages |
| Text Chunking | O(n) | n = chars |
| Embedding (1 text) | ~100ms | API latency |
| Embedding (batch) | ~500ms | 100 texts |
| Vector Add | O(1) | Per vector |
| Vector Search | O(n) | n = stored vectors |
| LLM Completion | ~2-5s | API latency |

### Space Complexity
| Component | Space | Notes |
|-----------|-------|-------|
| 1 Document (100 pages) | ~500KB | Text |
| 1 Chunk | ~1KB | Text |
| 1 Embedding | ~6KB | 1536 floats |
| 100 Documents | ~600MB | Vectors |

## 🔍 Error Handling Flow

```
User Action
    ↓
Try Operation
    ↓
    ├─→ Success
    │   └─→ Continue
    │
    └─→ Error
        ↓
        ├─→ File Error
        │   └─→ Show: "Invalid file format"
        │
        ├─→ API Error
        │   └─→ Show: "API key invalid"
        │
        ├─→ Processing Error
        │   └─→ Show: "Failed to process document"
        │
        └─→ General Error
            └─→ Show: Error message + suggestion
```

## 🎯 Key Decision Points

### 1. Which Vector Store?
```
FAISS:
✅ Faster search
✅ Less disk space
❌ Manual persistence

ChromaDB:
✅ Auto-persistence
✅ More features
❌ Slightly slower
```

### 2. Which Embedding Model?
```
text-embedding-3-small:
✅ Fast
✅ Cheap ($0.00002/1K)
✅ Good quality

text-embedding-3-large:
✅ Better quality
❌ 2x more expensive
❌ Slower
```

### 3. Which Chat Model?
```
GPT-4o:
✅ Best quality
✅ Latest model
❌ Most expensive

GPT-4-turbo:
✅ Fast
✅ Good quality
✅ Cheaper than GPT-4o

GPT-3.5-turbo:
✅ Very cheap
✅ Very fast
❌ Lower quality
```

---

**This architecture provides a scalable, maintainable, and efficient RAG system! 🚀**
