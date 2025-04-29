# 💡 RAG Knowledge Assistant

A full-stack Retrieval-Augmented Generation (RAG) application that:
- Ingests scientific papers (e.g., ArXiv data)
- Embeds them into a vector database (ChromaDB)
- Serves a FastAPI backend to answer queries based on retrieved context
- Provides a React frontend for users to interact and ask questions

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

## 🛠️ Backend Setup (FastAPI)

1. **Install dependencies** (in your Python virtual environment):

```bash
pip install -r requirements.txt
```

2. **Prepare Environment Variables**:

Create a `.env` at the project root:

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

