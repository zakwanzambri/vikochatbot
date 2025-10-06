# 🔄 OpenAI Alternatives - Integration Guide

This guide shows you how to switch from OpenAI to alternative AI providers.

## 📊 Quick Comparison

| Provider | Chat | Embeddings | Cost | Setup Difficulty |
|----------|------|------------|------|------------------|
| **OpenAI** (current) | ✅ | ✅ | $$$ | Easy |
| **Google Gemini** | ✅ | ✅ | FREE/$ | Easy |
| **Anthropic Claude** | ✅ | ❌ | $$ | Easy |
| **Ollama** (Local) | ✅ | ✅ | FREE | Medium |
| **Mistral AI** | ✅ | ✅ | $$ | Easy |

## 🚀 Option 1: Google Gemini (Recommended - FREE!)

### Advantages:
- ✅ FREE tier available
- ✅ 1 MILLION token context window
- ✅ Has both chat AND embeddings
- ✅ Very fast (Flash model)
- ✅ Good quality

### Setup:

**1. Get API Key:**
- Go to: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the key

**2. Install Package:**
```bash
pip install google-generativeai
```

**3. Update `.env`:**
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

**4. Update `src/config.py`:**
```python
# Change from OpenAI to Gemini
AI_PROVIDER = "gemini"  # Options: "openai", "gemini", "claude", "ollama"

# Gemini settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_CHAT_MODEL = "gemini-1.5-flash"  # or "gemini-1.5-pro"
```

**5. Update imports in your code:**
```python
# In src/ui/streamlit_app.py
from src.llm.gemini_integration import GeminiEmbedder, GeminiChat

# Replace OpenAI with Gemini
embedder = GeminiEmbedder()
chatbot = GeminiChat()
```

---

## 🤖 Option 2: Anthropic Claude (Best Quality)

### Advantages:
- ✅ Excellent response quality
- ✅ 200K token context
- ✅ Better at following instructions
- ⚠️ Need separate embeddings (use OpenAI or Cohere)

### Setup:

**1. Get API Key:**
- Go to: https://console.anthropic.com/
- Sign up and get API key

**2. Install Package:**
```bash
pip install anthropic
```

**3. Update `.env`:**
```bash
ANTHROPIC_API_KEY=your_claude_api_key_here
# Keep OpenAI key for embeddings
OPENAI_API_KEY=your_openai_key_here
```

**4. Mixed Setup (Claude + OpenAI Embeddings):**
```python
# In your code
from src.embedding.embedder import OpenAIEmbedder  # For embeddings
from src.llm.claude_integration import ClaudeChat   # For chat

embedder = OpenAIEmbedder()  # Still use OpenAI for embeddings
chatbot = ClaudeChat()       # Use Claude for chat
```

---

## 💻 Option 3: Ollama (Local/FREE - No API Costs!)

### Advantages:
- ✅ 100% FREE (no API costs!)
- ✅ Complete privacy (runs locally)
- ✅ No rate limits
- ✅ No internet required
- ⚠️ Requires decent GPU

### Setup:

**1. Install Ollama:**
- Download from: https://ollama.ai
- Install on your computer

**2. Pull Models:**
```bash
# Chat model
ollama pull llama3.1

# Embedding model
ollama pull nomic-embed-text
```

**3. Update `src/config.py`:**
```python
AI_PROVIDER = "ollama"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_CHAT_MODEL = "llama3.1"  # or "mistral", "phi3"
OLLAMA_EMBED_MODEL = "nomic-embed-text"
```

**4. Update imports:**
```python
from src.llm.ollama_integration import OllamaEmbedder, OllamaChat

embedder = OllamaEmbedder()
chatbot = OllamaChat()
```

---

## 🔧 Universal Integration Method

To make switching easy, update your `src/config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# AI Provider Selection
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # openai, gemini, claude, ollama

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o"

# Google Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_CHAT_MODEL = "gemini-1.5-flash"

# Anthropic Claude Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_CHAT_MODEL = "llama3.1"
OLLAMA_EMBED_MODEL = "nomic-embed-text"
```

Then in `.env`:
```bash
# Choose your provider
AI_PROVIDER=gemini

# Add relevant API keys
GOOGLE_API_KEY=your_key_here
# or
# ANTHROPIC_API_KEY=your_key_here
# or
# OPENAI_API_KEY=your_key_here
```

---

## 💰 Cost Comparison (per 1M tokens)

| Provider | Input | Output | Embeddings |
|----------|-------|--------|------------|
| **OpenAI GPT-4o** | $2.50 | $10.00 | $0.02 |
| **OpenAI GPT-3.5** | $0.50 | $1.50 | $0.02 |
| **Google Gemini Flash** | FREE | FREE | FREE |
| **Google Gemini Pro** | $1.25 | $5.00 | FREE |
| **Claude 3.5 Sonnet** | $3.00 | $15.00 | N/A |
| **Ollama (Local)** | FREE | FREE | FREE |

---

## 🎯 My Recommendation

### For You Right Now:
**Use Google Gemini!**

**Why?**
1. ✅ Has FREE tier (perfect for learning/testing)
2. ✅ Includes both chat AND embeddings
3. ✅ Easiest migration from OpenAI
4. ✅ Excellent quality
5. ✅ Huge context window (1M tokens!)

### Steps:
```bash
# 1. Install
pip install google-generativeai

# 2. Get free API key
# Visit: https://makersuite.google.com/app/apikey

# 3. Add to .env
GOOGLE_API_KEY=your_key_here

# 4. Use Gemini integration files I created
```

---

## 📝 Quick Start with Gemini

I've already created the integration files for you! Just:

1. Install: `pip install google-generativeai`
2. Get API key from Google
3. Add to `.env`: `GOOGLE_API_KEY=your_key`
4. That's it!

**Ready to switch? Let me know and I'll update your code!** 🚀
