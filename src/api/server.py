# src/api/server.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

class QueryRequest(BaseModel):
    """Request model for query endpoint"""
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    """Response model for query endpoint"""
    answer: str
    context_chunks: List[Dict[str, Any]]
    query: str

class APIServer:
    """
    FastAPI server for the RAG application.
    """
    
    def __init__(self, embedding_model, vector_store, llm_interface):
        """Initialize the API server with injected components"""
        self.app = FastAPI(
            title="RAG Knowledge Assistant API",
            description="API for the RAG Knowledge Assistant",
            version="1.0.0"
        )

        # Inject components
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.llm_interface = llm_interface

        # Register routes
        self._register_routes()

        # Configure CORS (important for frontend React app)
        self._configure_cors()

    def _register_routes(self):
        """Register API routes"""

        @self.app.get("/")
        async def root():
            return {"message": "RAG Knowledge Assistant API is running"}

        @self.app.post("/api/query", response_model=QueryResponse)
        async def query(request: QueryRequest):
            try:
                # Generate query embedding
                query_embedding = self.embedding_model.embed_query(request.query)

                # Retrieve relevant chunks
                context_chunks = self.vector_store.query(
                    query_embedding=query_embedding,
                    n_results=request.top_k
                )

                # Generate response
                answer = self.llm_interface.generate_response(
                    query=request.query,
                    context_chunks=context_chunks
                )

                return {
                    "answer": answer,
                    "context_chunks": context_chunks,
                    "query": request.query
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/health")
        async def health_check():
            return {"status": "healthy"}

    def _configure_cors(self):
        """Configure CORS to allow frontend requests"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the API server"""
        uvicorn.run(self.app, host=host, port=port)

# For ASGI servers
app_instance = None
app = None

def create_app(embedding_model, vector_store, llm_interface):
    global app_instance, app
    app_instance = APIServer(embedding_model, vector_store, llm_interface)
    app = app_instance.app
    return app
