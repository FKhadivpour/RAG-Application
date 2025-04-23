from typing import List, Dict, Any, Optional
import os
import chromadb
import numpy as np

class VectorStore:
    """
    Manages vector storage and retrieval using ChromaDB.
    """
    
    def __init__(self, persist_directory: Optional[str] = None, collection_name: str = "documents"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection to use
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        
    def initialize(self):
        """
        Initialize the ChromaDB client and collection.
        """
        if self.client is None:
            if self.persist_directory:
                os.makedirs(self.persist_directory, exist_ok=True)
                self.client = chromadb.PersistentClient(path=self.persist_directory)
            else:
                self.client = chromadb.Client()
                
            # Get or create collection
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                print(f"Using existing collection: {self.collection_name}")
            except Exception:
                self.collection = self.client.create_collection(name=self.collection_name)
                print(f"Created new collection: {self.collection_name}")
    
    def add_embeddings(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Add document chunks with embeddings to the vector store.
        
        Args:
            chunks: List of chunk dictionaries with text, metadata, and embeddings
        """
        if not chunks:
            print("No chunks to add to vector store")
            return
            
        if self.collection is None:
            self.initialize()
            
        # Prepare data for ChromaDB
        ids = [chunk["metadata"]["chunk_id"] for chunk in chunks]
        embeddings = [chunk["embedding"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
        print(f"Added {len(chunks)} chunks to vector store")
    
    def query(self, query_embedding: np.ndarray, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            
        Returns:
            List of similar document chunks
        """
        if self.collection is None:
            self.initialize()
            
        # Convert numpy array to list for ChromaDB
        if isinstance(query_embedding, np.ndarray):
            query_embedding = query_embedding.tolist()
            
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["ids"][0])):
            result = {
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results.get("distances", [[]])[0][i] if "distances" in results else None
            }
            formatted_results.append(result)
            
        return formatted_results
