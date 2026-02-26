<p align="center">
  <h1 align="center">🤖 AI Writer — Advanced Text Summarization</h1>
  <p align="center">
    An intelligent text summarization web application powered by state-of-the-art NLP models via the Hugging Face Inference API.
  </p>
  <p align="center">
    <a href="#features">Features</a> •
    <a href="#demo">Demo</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#api-reference">API Reference</a> •
    <a href="#testing">Testing</a> •
    <a href="#deployment">Deployment</a> •
    <a href="#contributing">Contributing</a>
  </p>
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running Locally](#running-locally)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Models](#models)
- [Testing](#testing)
- [Deployment](#deployment)
- [Performance & Caching](#performance--caching)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

**AI Writer** is a full-stack web application that provides abstractive text summarization using transformer-based NLP models. Users can paste text or upload PDF documents and receive concise, AI-generated summaries along with extracted keywords and readability metrics.

The application leverages the [Hugging Face Inference API](https://huggingface.co/docs/api-inference/) for model inference, eliminating the need for local GPU resources while delivering high-quality summarization results.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Dual Model Support** | Choose between Standard (fast) and Pro (advanced) summarization models |
| **Adjustable Summary Length** | Short, Medium, or Detailed output based on your needs |
| **PDF Upload** | Extract and summarize text directly from PDF documents |
| **Text Input** | Paste any text for instant summarization |
| **Keyword Extraction** | Automatic TF-IDF based keyword extraction from input text |
| **Readability Metrics** | Input/summary word counts, compression ratio, and Flesch Reading Ease score |
| **Response Caching** | Built-in caching to avoid redundant API calls for identical inputs |
| **Long Document Chunking** | Automatic text chunking for documents exceeding model token limits |
| **Error Handling** | Inline error messages displayed directly in the UI |
| **Responsive UI** | Clean, modern Bootstrap 5 interface |

---

## 🖥️ Demo

<p align="center">
  <img src="https://img.shields.io/badge/Status-Live-brightgreen" alt="Status" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/Framework-Flask-lightgrey" alt="Flask" />
  <img src="https://img.shields.io/badge/API-Hugging%20Face-yellow" alt="HuggingFace" />
</p>

**Input**: Paste text or upload a PDF → **Select** model & length → **Click** Summarize → **Get** summary, keywords, and metrics.

---

## 🏗️ Architecture

```
┌────────────────────────┐
│     Browser (UI)       │
│  Bootstrap 5 + Fetch   │
└───────────┬────────────┘
            │ HTTP POST /summarize
            ▼
┌────────────────────────┐
│   Flask Backend        │
│  ┌──────────────────┐  │
│  │  app.py (Routes) │  │
│  └────────┬─────────┘  │
│           │             │
│  ┌────────▼─────────┐  │
│  │ summarizer.py    │──┼──► Hugging Face Inference API
│  │ (HF API Client)  │  │    ┌─────────────────────────┐
│  └──────────────────┘  │    │ distilbart-cnn-12-6     │
│                         │    │ bart-large-cnn          │
│  ┌──────────────────┐  │    └─────────────────────────┘
│  │ utils.py         │  │
│  │ (PDF, Keywords,  │  │
│  │  Metrics)        │  │
│  └──────────────────┘  │
│                         │
│  ┌──────────────────┐  │
│  │ Flask-Caching    │  │
│  │ (SimpleCache)    │  │
│  └──────────────────┘  │
└────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Core language |
| **Flask** | Web framework & REST API |
| **Flask-Caching** | In-memory response caching |
| **Requests** | HTTP client for HF API |
| **pdfplumber** | PDF text extraction |
| **scikit-learn** | TF-IDF keyword extraction |
| **textstat** | Readability scoring (Flesch Reading Ease) |
| **Gunicorn** | Production WSGI server |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **HTML5** | Page structure |
| **Bootstrap 5** | Responsive UI framework |
| **JavaScript (Vanilla)** | Async form submission & DOM manipulation |

### External Services
| Service | Purpose |
|---------|---------|
| **Hugging Face Inference API** | Remote model inference for summarization |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- **pip** package manager
- **Hugging Face API Token** ([Get one free here](https://huggingface.co/settings/tokens))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbhiAJ001/AI-Writer-with-Advanced-Text-Summarization.git
   cd AI-Writer-with-Advanced-Text-Summarization
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HF_API_TOKEN` | ✅ Yes | Your Hugging Face API token for model inference |
| `SKIP_MODEL_LOAD` | ❌ No | Set to `true` to skip model loading on startup (default: `false`) |

**Set the environment variable:**

```bash
# Linux / macOS
export HF_API_TOKEN=hf_your_token_here

# Windows (Command Prompt)
set HF_API_TOKEN=hf_your_token_here

# Windows (PowerShell)
$env:HF_API_TOKEN="hf_your_token_here"
```

### Running Locally

```bash
python app.py
```

The app will start on **http://localhost:5000**.

---

## 📁 Project Structure

```
AI-Writer-with-Advanced-Text-Summarization/
│
├── app.py                  # Flask application entry point & API routes
├── summarizer.py           # HF Inference API client & summarization logic
├── utils.py                # Utility functions (PDF extraction, keywords, metrics)
├── requirements.txt        # Python dependencies
├── Procfile                # Heroku/production deployment config
│
├── templates/
│   └── index.html          # Frontend UI (Bootstrap 5)
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py         # Integration tests for Flask routes
│   └── test_logic.py       # Unit tests for utility & summarizer functions
│
└── uploads/                # Temporary directory for PDF uploads
```

---

## 📡 API Reference

### `GET /`
Renders the main web interface.

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Writer API"
}
```

### `POST /summarize`
Summarizes text or PDF content.

**Request (Form Data):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | ✅* | Raw text to summarize |
| `file` | file | ✅* | PDF file to summarize |
| `model` | string | ❌ | `standard` (default) or `pro` |
| `length` | string | ❌ | `short`, `medium` (default), or `detailed` |

> \* Either `text` or `file` must be provided, not both.

**Request (JSON):**
```json
{
  "text": "Your long text to summarize...",
  "model": "standard",
  "length": "medium"
}
```

**Success Response (200):**
```json
{
  "summary": "Concise summary of the input text...",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "metrics": {
    "input_word_count": 250,
    "summary_word_count": 45,
    "compression_ratio": 82.0,
    "readability_score": 65.3
  }
}
```

**Error Response (400/500):**
```json
{
  "error": "Text too short to summarize"
}
```

---

## 🧠 Models

| Mode | Model | Description | Speed |
|------|-------|-------------|-------|
| **Standard** | [`sshleifer/distilbart-cnn-12-6`](https://huggingface.co/sshleifer/distilbart-cnn-12-6) | Distilled BART model fine-tuned on CNN/DailyMail. Lightweight and fast. | ⚡ Fast |
| **Pro** | [`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn) | Full BART-Large model fine-tuned on CNN/DailyMail. Higher accuracy. | 🐢 Slower |

### Summary Length Settings

| Setting | Min Length | Max Length | Use Case |
|---------|-----------|-----------|----------|
| **Short** | 30 tokens | 150 tokens | Quick overviews, key takeaways |
| **Medium** | 80 tokens | 300 tokens | Balanced summaries (default) |
| **Detailed** | 150 tokens | 500 tokens | Comprehensive coverage |

---

## 🧪 Testing

The project includes both unit tests and integration tests.

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_app.py -v      # Integration tests
python -m pytest tests/test_logic.py -v    # Unit tests
```

### Test Coverage

| Test File | Coverage |
|-----------|----------|
| `test_app.py` | Health check, index page, text summarization, PDF upload, input validation |
| `test_logic.py` | Text cleaning, keyword extraction, metrics calculation, generation params, text chunking |

---

## 🚢 Deployment

### Heroku

The project includes a `Procfile` for Heroku deployment:

```
web: gunicorn app:app
```

**Deploy steps:**
```bash
heroku create your-app-name
heroku config:set HF_API_TOKEN=hf_your_token_here
git push heroku main
```

### Docker (Optional)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV HF_API_TOKEN=""
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

```bash
docker build -t ai-writer .
docker run -p 5000:5000 -e HF_API_TOKEN=hf_your_token ai-writer
```

---

## ⚡ Performance & Caching

- **Response caching** is enabled via `Flask-Caching` with `SimpleCache` backend (300s TTL)
- Cache keys are computed using `MD5(text) + model + length` to ensure unique cache entries
- **Text chunking** handles long documents by splitting into model-appropriate chunk sizes:
  - Standard model: 3,000 characters per chunk
  - Pro model: 4,000 characters per chunk
- **API timeout**: 120 seconds per request with `wait_for_model: true` to handle cold starts

---

## 🗺️ Roadmap

- [ ] Add support for more file formats (DOCX, TXT)
- [ ] Implement user authentication & history
- [ ] Add summary comparison between models
- [ ] Support multi-language summarization
- [ ] Add a copy-to-clipboard button for summaries
- [ ] Integrate with Google Gemini API as an alternative backend
- [ ] Add batch processing for multiple documents
- [ ] Progressive summarization for very long documents

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions
- Write tests for new features

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Hugging Face](https://huggingface.co/) — Inference API and transformer models
- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [Bootstrap](https://getbootstrap.com/) — Frontend UI framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction
- [textstat](https://github.com/textstat/textstat) — Text readability analysis
- [scikit-learn](https://scikit-learn.org/) — TF-IDF keyword extraction

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/AbhiAJ001">AbhiAJ001</a>
</p>
