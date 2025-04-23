import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

from src.data_processing import DocumentProcessor
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.llm import LLMInterface
from src.api import APIServer

def main():
    """
    Main entry point for the RAG Knowledge Assistant application.
    """
    print("Starting RAG Knowledge Assistant...")
    
    # Initialize components
    print("Initializing components...")
    document_processor = DocumentProcessor()
    embedding_model = EmbeddingModel()
    vector_store = VectorStore(persist_directory="data/vector_store")
    llm_interface = LLMInterface()
    
    # Check if we need to process documents
    if len(sys.argv) > 1 and sys.argv[1] == "--process-data":
        print("Processing documents...")
        data_dir = os.getenv("DATA_DIR", "data/raw")
        output_dir = os.getenv("OUTPUT_DIR", "data/processed")
        
        # Load and process documents
        documents = document_processor.load_documents(data_dir)
        chunks = document_processor.chunk_documents(documents)
        
        # Generate embeddings
        embedding_model.load_model()
        chunks_with_embeddings = embedding_model.embed_chunks(chunks)
        
        # Save processed chunks
        document_processor.save_processed_chunks(chunks_with_embeddings, output_dir)
        
        # Add to vector store
        vector_store.initialize()
        vector_store.add_embeddings(chunks_with_embeddings)
        
        print(f"Processed {len(documents)} documents into {len(chunks)} chunks")
    
    # Start API server
    print("Starting API server...")
    api_server = APIServer()
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    api_server.run(host=host, port=port)

if __name__ == "__main__":
    main()
