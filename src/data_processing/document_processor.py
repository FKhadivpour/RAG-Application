import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

class DocumentProcessor:
    """
    Handles document loading, chunking, and preprocessing for the RAG pipeline.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: The size of text chunks in characters
            chunk_overlap: The overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load_documents(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Load documents from a directory.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of document dictionaries with text and metadata
        """
        documents = []
        directory = Path(directory_path)
        
        for file_path in directory.glob("**/*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Extract relevant fields from ArXiv papers
                doc = {
                    "id": data.get("id", ""),
                    "title": data.get("title", ""),
                    "abstract": data.get("abstract", ""),
                    "authors": data.get("authors", []),
                    "categories": data.get("categories", []),
                    "text": data.get("abstract", ""),  # Start with abstract as text
                    "source": str(file_path)
                }
                
                documents.append(doc)
            except Exception as e:
                print(f"Error loading document {file_path}: {e}")
        
        print(f"Loaded {len(documents)} documents from {directory_path}")
        return documents
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Split documents into smaller chunks for processing.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        
        for doc in documents:
            text = doc.get("text", "")
            
            # Skip empty documents
            if not text.strip():
                continue
                
            # Create chunks with overlap
            doc_chunks = self._create_chunks(text, self.chunk_size, self.chunk_overlap)
            
            # Create chunk objects with metadata
            for i, chunk_text in enumerate(doc_chunks):
                chunk = {
                    "text": chunk_text,
                    "metadata": {
                        "doc_id": doc.get("id", ""),
                        "title": doc.get("title", ""),
                        "chunk_id": f"{doc.get('id', '')}-{i}",
                        "chunk_index": i,
                        "source": doc.get("source", ""),
                        "authors": doc.get("authors", []),
                        "categories": doc.get("categories", [])
                    }
                }
                chunks.append(chunk)
        
        print(f"Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks
    
    def _create_chunks(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """
        Create overlapping chunks from text.
        
        Args:
            text: The text to chunk
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        end = chunk_size
        
        while start < len(text):
            # Adjust chunk end to not cut words
            if end < len(text):
                # Try to find a good breaking point
                while end > start and end < len(text) and text[end] not in ['.', '!', '?', '\n']:
                    end += 1
                
                # If we couldn't find a good breaking point, just use the original end
                if end - start >= chunk_size * 1.5:
                    end = start + chunk_size
            
            # Extract the chunk
            chunk = text[start:min(end + 1, len(text))].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move to next chunk with overlap
            start = end - chunk_overlap
            end = start + chunk_size
        
        return chunks
    
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Placeholder for embedding chunks.
        This would be implemented by the embedding module.
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            List of chunks with embeddings added
        """
        # This is a placeholder - actual embedding happens in the embedding module
        print(f"Prepared {len(chunks)} chunks for embedding")
        return chunks
    
    def save_processed_chunks(self, chunks: List[Dict[str, Any]], output_dir: str) -> None:
        """
        Save processed chunks to disk.
        
        Args:
            chunks: List of chunk dictionaries
            output_dir: Directory to save processed chunks
        """
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "processed_chunks.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2)
            
        print(f"Saved {len(chunks)} processed chunks to {output_path}")
