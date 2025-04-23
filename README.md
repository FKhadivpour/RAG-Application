# RAG Knowledge Assistant

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

### Installation

1. Clone the repository
```bash
git clone https://github.com/fkhadivpour/rag-knowledge-assistant.git
cd rag-knowledge-assistant
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

4. Install frontend dependencies
```bash
cd frontend
npm install
cd ..
```

### Running the Application

#### Development Mode

1. Start the backend server
```bash
python -m src.main
```

2. Start the frontend development server
```bash
cd frontend
npm start
```

3. Access the application at http://localhost:3000

#### Using Docker

```bash
docker-compose up
```

## Project Structure

```
rag-knowledge-assistant/
├── data/                  # Data storage and processing
│   ├── raw/               # Raw document storage
│   └── processed/         # Processed chunks and metadata
├── src/                   # Backend source code
│   ├── data_processing/   # Document ingestion and processing
│   ├── embeddings/        # Embedding models and utilities
│   ├── vector_store/      # Vector database integration
│   ├── llm/               # LLM integration and prompt templates
│   ├── api/               # FastAPI routes and middleware
│   └── evaluation/        # Performance evaluation tools
├── frontend/              # React frontend application
├── tests/                 # Test suite
├── notebooks/             # Jupyter notebooks for exploration
├── docker/                # Docker configuration
└── scripts/               # Utility scripts
```

## Usage Examples

### Document Ingestion

```python
from src.data_processing import DocumentProcessor
from src.vector_store import VectorStore

# Process documents and store in vector database
processor = DocumentProcessor()
documents = processor.load_documents("data/raw/papers/")
chunks = processor.chunk_documents(documents)
embeddings = processor.embed_chunks(chunks)

# Store in vector database
vector_store = VectorStore()
vector_store.add_embeddings(embeddings, chunks)
```

### Query Processing

```python
from src.api.query_engine import QueryEngine
from src.llm import LLMInterface

# Set up query engine and LLM
query_engine = QueryEngine()
llm = LLMInterface()

# Process a user query
user_query = "What are the latest developments in transformer architectures?"
relevant_chunks = query_engine.retrieve_relevant_chunks(user_query)
response = llm.generate_response(user_query, relevant_chunks)
print(response)
```

## Evaluation

The repository includes evaluation scripts to measure:

- Retrieval precision and recall
- Answer relevance and accuracy
- Response latency
- User satisfaction metrics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ArXiv for providing the dataset
- The open-source community for the amazing tools and libraries that make this project possible
