# 🎯 Getting Started - Step by Step

Welcome to your Document Q&A Chatbot! Follow these steps to get up and running.

## ⚡ Quick Start (3 Steps)

### 1️⃣ Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2️⃣ Set Up API Key
```powershell
# Copy the example file
copy .env.example .env

# Edit .env and add your OpenAI API key
# Get your key from: https://platform.openai.com/api-keys
```

### 3️⃣ Run the App
```powershell
# Option 1: Use the batch file (Windows)
run.bat

# Option 2: Run directly
streamlit run src/ui/streamlit_app.py
```

## 📋 Detailed Setup

### Prerequisites Check
- ✅ Python 3.8 or higher
- ✅ pip package manager
- ✅ OpenAI API key
- ✅ Internet connection

### Step 1: Verify Installation
```powershell
# Check Python version
python --version

# Should show Python 3.8.x or higher
```

### Step 2: Install Packages
```powershell
# Navigate to project directory
cd c:\xampp\htdocs\vikochatbot

# Install all requirements
pip install -r requirements.txt

# Verify installation (optional)
python setup_check.py
```

### Step 3: Configure Environment
```powershell
# Copy environment template
copy .env.example .env

# Open .env in your favorite editor
notepad .env

# Replace the placeholder with your actual API key:
# OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 4: Run Setup Check
```powershell
python setup_check.py
```

This will verify:
- ✅ Python version
- ✅ All packages installed
- ✅ Directory structure
- ✅ Core files present
- ✅ Environment configured

### Step 5: Launch Application

**Option A: Using batch file (Easiest)**
```powershell
run.bat
```

**Option B: Direct Streamlit command**
```powershell
streamlit run src/ui/streamlit_app.py
```

**Option C: Custom port**
```powershell
streamlit run src/ui/streamlit_app.py --server.port 8502
```

The app will open automatically in your browser at:
- Default: http://localhost:8501
- Custom: http://localhost:8502 (if you changed the port)

## 📚 Using the Chatbot

### Upload Documents
1. Click **"Browse files"** in the left sidebar
2. Select PDF, DOCX, or TXT files
3. Click **"🔄 Process Documents"**
4. Wait for the progress bar to complete

### Ask Questions
1. Type your question in the chat box at the bottom
2. Press **Enter** or click the send button
3. View the AI-generated answer with source citations
4. See which documents were used to answer

### Manage Your Database
- **Load Existing**: Resume with previously uploaded documents
- **Clear Database**: Start fresh, removes all data
- **Clear Chat**: Reset conversation history

## 🔧 Configuration

### Change Models
Edit `src/config.py`:
```python
# Use different OpenAI models
EMBEDDING_MODEL = "text-embedding-3-small"  # or text-embedding-3-large
CHAT_MODEL = "gpt-4o"  # or gpt-4-turbo, gpt-3.5-turbo
```

### Adjust Chunking
Edit `src/config.py`:
```python
CHUNK_SIZE = 1000      # Smaller = more precise, Larger = more context
CHUNK_OVERLAP = 200    # How much chunks overlap
```

### Change Vector Store
Edit `src/config.py`:
```python
VECTOR_STORE_TYPE = "faiss"  # or "chroma"
```

### Retrieval Settings
Edit `src/config.py`:
```python
TOP_K_RESULTS = 5  # How many document chunks to retrieve
```

## 🧪 Testing Your Setup

### Test 1: Upload a Sample Document
1. Create a test.txt file with some content:
   ```
   The Document Q&A Chatbot is an AI-powered system that answers questions
   based on uploaded documents. It uses RAG (Retrieval-Augmented Generation)
   to provide accurate, source-cited answers.
   ```
2. Upload this file through the interface
3. Process it

### Test 2: Ask Questions
Try these questions:
- "What is the Document Q&A Chatbot?"
- "What technology does it use?"
- "How does it provide answers?"

### Test 3: Check Sources
Verify that the answer includes:
- ✅ Relevant information from your document
- ✅ Source citation showing "test.txt"
- ✅ Confidence score

## ❓ Troubleshooting

### Issue: "Module not found"
```powershell
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: "OpenAI API key not found"
```powershell
# Solution: Check .env file
1. Verify .env exists in project root
2. Open .env and check OPENAI_API_KEY=sk-...
3. Make sure no extra spaces or quotes
4. Restart the application
```

### Issue: "FAISS installation failed"
```powershell
# Solution 1: Try without cache
pip install faiss-cpu --no-cache-dir

# Solution 2: Use ChromaDB instead
# Edit src/config.py and set:
VECTOR_STORE_TYPE = "chroma"
```

### Issue: "Streamlit not found"
```powershell
# Solution: Install streamlit specifically
pip install streamlit
```

### Issue: Port already in use
```powershell
# Solution: Use different port
streamlit run src/ui/streamlit_app.py --server.port 8502
```

### Issue: "No module named 'src'"
```powershell
# Solution: Make sure you're in the project directory
cd c:\xampp\htdocs\vikochatbot

# Then run the app
streamlit run src/ui/streamlit_app.py
```

## 💡 Tips for Best Results

### Document Quality
- ✅ Use clear, well-formatted documents
- ✅ PDFs with selectable text (not scanned images)
- ✅ DOCX with proper structure
- ✅ UTF-8 encoded text files

### Question Types
- ✅ **Good**: "What are the main features of the product?"
- ✅ **Good**: "How does the authentication work?"
- ❌ **Bad**: "Tell me everything" (too broad)
- ❌ **Bad**: "Is this good?" (subjective)

### Performance
- ✅ Upload related documents together
- ✅ Clear database periodically
- ✅ Use specific questions for better results
- ✅ Check source citations for accuracy

## 🎓 Next Steps

### Learn More
- 📖 Read `README.md` for full features
- 🔧 Read `IMPLEMENTATION.md` for technical details
- 📚 Check `QUICKSTART.md` for quick reference

### Customize
- 🎨 Modify `src/ui/streamlit_app.py` for UI changes
- ⚙️ Adjust `src/config.py` for behavior
- 🔧 Extend `src/` modules for new features

### Advanced Usage
```python
# Use programmatically
from src.document_processor import PDFExtractor
from src.embedding import OpenAIEmbedder, TextChunker
from src.vector_store import FAISSVectorStore
from src.retrieval import DocumentRetriever
from src.llm import ChatBot

# Process documents
extractor = PDFExtractor()
data = extractor.extract_text("document.pdf")

# Create embeddings
chunker = TextChunker()
chunks = chunker.chunk_text(data['text'])

embedder = OpenAIEmbedder()
embedded_chunks = embedder.embed_chunks(chunks)

# Store and retrieve
vector_store = FAISSVectorStore()
vector_store.add_documents(embedded_chunks)

retriever = DocumentRetriever(vector_store, embedder)
chatbot = ChatBot()

# Ask questions
result = chatbot.chat_with_retrieval("Your question?", retriever)
print(result['answer'])
```

## 🆘 Getting Help

### Resources
- 📧 Check error messages carefully
- 🔍 Search issues in the code
- 📝 Check configuration files
- 🌐 Review OpenAI documentation

### Common Fixes
```powershell
# Reset everything
run.bat  # Will check setup first

# Verify setup
python setup_check.py

# Check Python packages
pip list | findstr "streamlit openai faiss"

# Test API key
python -c "from src.config import OPENAI_API_KEY; print('OK' if OPENAI_API_KEY else 'Missing')"
```

## 🎉 You're Ready!

Your Document Q&A Chatbot is now set up and ready to use!

**Start the app:**
```powershell
run.bat
```

**Or:**
```powershell
streamlit run src/ui/streamlit_app.py
```

Enjoy your intelligent document assistant! 📚🤖
