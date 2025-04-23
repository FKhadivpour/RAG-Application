from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    """
    Handles text embedding using Sentence Transformers.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model_name = model_name
        self.model = None
        
    def load_model(self):
        """
        Load the embedding model.
        """
        if self.model is None:
            try:
                self.model = SentenceTransformer(self.model_name)
                print(f"Loaded embedding model: {self.model_name}")
            except Exception as e:
                print(f"Error loading embedding model: {e}")
                raise
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            Array of embeddings
        """
        if self.model is None:
            self.load_model()
            
        try:
            embeddings = self.model.encode(texts, show_progress_bar=True)
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise
    
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for a list of document chunks.
        
        Args:
            chunks: List of chunk dictionaries with text and metadata
            
        Returns:
            List of chunks with embeddings added
        """
        if not chunks:
            return []
            
        # Extract text from chunks
        texts = [chunk["text"] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.embed_texts(texts)
        
        # Add embeddings to chunks
        for i, chunk in enumerate(chunks):
            chunk["embedding"] = embeddings[i].tolist()
            
        print(f"Generated embeddings for {len(chunks)} chunks")
        return chunks
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a query string.
        
        Args:
            query: Query text
            
        Returns:
            Query embedding
        """
        if self.model is None:
            self.load_model()
            
        try:
            embedding = self.model.encode(query)
            return embedding
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            raise
