# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/zakwanzambri/vikochatbot.git
cd vikochatbot
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

### Step 1: Configure API Key
- In the sidebar, enter your OpenAI API key
- The key is password-protected and not stored

### Step 2: Upload Documents
- Click "Browse files" or drag and drop
- Supported formats: PDF, DOCX, TXT
- You can upload multiple files at once

### Step 3: Process Documents
- Click the "🔄 Process Documents" button
- Wait for processing to complete
- You'll see a success message with the number of processed files

### Step 4: Ask Questions
- Type your question in the chat input at the bottom
- Press Enter or click the send button
- The chatbot will answer based on your documents
- If the info isn't found, it will let you know

## Example Questions

After uploading a company document, you might ask:
- "What is the company's revenue?"
- "Who founded the company?"
- "What products does the company offer?"
- "Where is the headquarters located?"

## Tips

- **Be specific**: Ask clear, specific questions for better answers
- **Context matters**: The chatbot remembers previous questions in the conversation
- **Document quality**: Better formatted documents = better answers
- **Multiple documents**: Upload all related documents at once for comprehensive answers

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "OpenAI API error"
- Check your API key is correct
- Verify you have API credits available
- Check your internet connection

### Documents not processing
- Ensure files are not corrupted
- Check file format is supported (PDF, DOCX, TXT)
- Try processing files one at a time

### Slow responses
- Large documents take longer to process
- OpenAI API may have rate limits
- Check your internet speed

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [IMPLEMENTATION.md](IMPLEMENTATION.md) for technical details
- Open an issue on GitHub for bugs or feature requests

## Security

- Never share your OpenAI API key
- API key is only used during your session
- Documents are processed in memory only
- No data is stored permanently
