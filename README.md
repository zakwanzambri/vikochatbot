# 🤖 Viko Chatbot - Intelligent Document-Based Q&A

Build a smart chatbot that can answer questions based on uploaded documents or notes (PDF, DOCX, TXT, etc.)

## 📋 Features

- **Multiple Document Support**: Upload PDF, DOCX, and TXT files
- **Intelligent Text Processing**: Extracts and cleans text from documents
- **Smart Chunking**: Splits documents into optimal chunks for better retrieval
- **Vector Embeddings**: Uses OpenAI embeddings for semantic search
- **FAISS Vector Store**: Efficient similarity search and retrieval
- **RAG (Retrieval-Augmented Generation)**: Combines document retrieval with GPT for accurate answers
- **Context-Aware Responses**: Answers based only on uploaded documents
- **User-Friendly UI**: Built with Streamlit for easy interaction
- **Chat History**: Maintains conversation context
- **Error Handling**: Returns "I couldn't find that info" when information is not available

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/zakwanzambri/vikochatbot.git
cd vikochatbot
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔑 Setup

1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Run the application (you'll enter the API key in the UI)

## 💻 Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. In the sidebar:
   - Enter your OpenAI API key
   - Upload one or more documents (PDF, DOCX, TXT)
   - Click "Process Documents"

3. Start asking questions about your documents in the chat interface!

## 📚 How It Works

1. **Document Upload**: Users upload PDF, DOCX, or TXT files
2. **Text Extraction**: Extracts and cleans text from documents
3. **Chunking**: Splits text into smaller chunks (1000 chars with 200 char overlap)
4. **Embeddings**: Generates vector embeddings using OpenAI API
5. **Vector Store**: Stores embeddings in FAISS for efficient retrieval
6. **Query Processing**: When user asks a question:
   - Converts question to embedding
   - Retrieves top 3 most relevant chunks
   - Sends context + question to GPT-3.5-turbo
   - Returns answer based only on document content
7. **Fallback**: If info not found, returns "I couldn't find that info"

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-3.5-turbo
- **Embeddings**: OpenAI text-embedding-ada-002
- **Vector Store**: FAISS
- **Document Processing**: PyPDF2, python-docx
- **Framework**: LangChain

## 📁 Project Structure

```
vikochatbot/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🔒 Security Notes

- Never commit your OpenAI API key to version control
- API key is entered via the UI and not stored
- Keep your `.env` files private if you choose to use them

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.
