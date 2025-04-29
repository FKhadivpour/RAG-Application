# 💡 RAG Knowledge Assistant

A Retrieval-Augmented Generation (RAG) application that leverages vector databases and large language models to provide accurate, context-aware responses based on specific knowledge domains.

## Overview

This repository implements a complete RAG pipeline with a user-friendly web interface. The system retrieves relevant information from a vector database containing embedded documents and uses this context to generate accurate responses through a large language model.

## Features

- **Document Processing Pipeline**: Ingest, chunk, and embed documents from various sources
- **Vector Database Integration**: Store and efficiently query document embeddings
- **Semantic Search**: Find the most relevant context for user queries
- **LLM Integration**: Generate contextually accurate responses using retrieved information
- **Web Interface**: User-friendly UI for interacting with the RAG system
- **API Endpoints**: RESTful API for programmatic access to the RAG pipeline
- **Performance Metrics**: Evaluation tools to measure retrieval and generation quality

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Data Ingestion │────▶│ Vector Database │────▶│  LLM Interface  │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       ▲                       │
        │                       │                       │
        ▼                       │                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│ Text Processing │     │  Query Engine   │◀────│   Web Server    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Dataset

This project uses the [ArXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv) containing scientific papers across various domains. The dataset provides rich, technical content perfect for demonstrating RAG capabilities in specialized knowledge retrieval.

## Technologies Used

- **Backend**: Python, FastAPI
- **Vector Database**: Chroma
- **Embeddings**: Sentence-Transformers
- **LLM Integration**: OpenAI API (with option for local models)
- **Frontend**: React with TypeScript
- **Containerization**: Docker
- **Testing**: Pytest



## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker (optional)

### 🛠️ Installation

1. Clone the repository
```bash
git clone https://github.com/fkhadivpour/RAG-Application.git
```

2. Set up the Python environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

```env
HOST=127.0.0.1
PORT=8000
DATA_DIR=data/raw
OUTPUT_DIR=data/processed
VECTOR_STORE_DIR=data/vector_store
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
OPENAI_API_KEY=your-openai-key-here
OPENAI_API_BASE=https://api.openai.com/v1
```

3. **Process Data** (one-time to populate vector store):

```bash
python main.py --process-data
```

4. **Start Backend Server**:

```bash
python main.py
```

Backend will run on:
```
http://127.0.0.1:8000
```

---

## 💾 Frontend Setup (React)

1. **Go to frontend folder**:

```bash
cd frontend
```

2. **Install dependencies**:

```bash
npm install
```

3. **Start Frontend Server**:

```bash
npm start
```

Frontend will open at:
```
http://localhost:3000
```

Frontend will automatically proxy API requests to backend (`http://localhost:8000`).

---

## 🚀 Usage Flow

- Open [http://localhost:3000](http://localhost:3000)
- Type a query related to your documents (e.g., "What is machine learning?")
- Click "Search"
- See AI-generated answer based on retrieved document context!

---




## 📂 Project Structure

```
RAG-Application/
├── data/
│   ├── raw/               # Raw ArXiv JSON documents
│   ├── processed/         # Processed chunks
│   └── vector_store/      # ChromaDB persisted vectors
├── docker/                # (empty) - reserved for Docker configs
├── notebooks/             # (empty) - reserved for experiments
├── scripts/               # (empty) - reserved for automation scripts
├── src/                   # Python backend source code
│   ├── api/
│   ├── data_processing/
│   ├── embeddings/
│   ├── llm/
│   ├── vector_store/
│   └── evaluation/        # (optional future) evaluation code
├── frontend/              # React frontend application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── .env               # Frontend-specific environment
├── .env                   # Backend-specific environment
├── main.py                # Backend entry point
└── README.md              # (this file)
```

---

## 📋 Notes

- Download the ArXiv dataset json file from kaggle into data/raw folder.
- Backend and Frontend must be running simultaneously in separate terminals.

---

## 📈 Future Improvements

- Add Docker support
- Add unit tests inside `/tests/`
- Improve frontend UI/UX
- Support PDF and DOCX ingestion

---

## 📝 Quick Developer Commands

| Action | Command |
|:-------|:--------|
| Process documents | `python main.py --process-data` |
| Start backend server | `python main.py` |
| Start frontend server | `npm start` (inside `frontend/`) |
| Fix npm vulnerabilities | `npm audit fix --force` (optional) |

---

# ✅ Full Stack Ready!

- FastAPI + ChromaDB + OpenAI + React.js
- Fully modular and professional RAG application
- Easy to extend, deploy, and scale

---

