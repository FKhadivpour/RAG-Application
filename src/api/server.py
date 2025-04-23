from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

from ..data_processing import DocumentProcessor
from ..embeddings import EmbeddingModel
from ..vector_store import VectorStore
from ..llm import LLMInterface

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
    
    def __init__(self):
        """Initialize the API server and components"""
        self.app = FastAPI(
            title="RAG Knowledge Assistant API",
            description="API for the RAG Knowledge Assistant",
            version="1.0.0"
        )
        
        # Initialize components
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(persist_directory="data/vector_store")
        self.llm_interface = LLMInterface()
        
        # Register routes
        self.register_routes()
        
    def register_routes(self):
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
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the API server"""
        uvicorn.run(self.app, host=host, port=port)

# Create app instance for ASGI servers
app_instance = APIServer()
app = app_instance.app

if __name__ == "__main__":
    app_instance.run()
