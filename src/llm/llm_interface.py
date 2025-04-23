from typing import List, Dict, Any, Optional
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMInterface:
    """
    Interface for interacting with Large Language Models.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the LLM interface.
        
        Args:
            model_name: Name of the LLM model to use
        """
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
    
    def generate_response(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate a response using the LLM with retrieved context.
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            
        Returns:
            Generated response
        """
        # Format context for the prompt
        formatted_context = self._format_context(context_chunks)
        
        # Create prompt with query and context
        prompt = self._create_prompt(query, formatted_context)
        
        # Call LLM API
        response = self._call_llm_api(prompt)
        
        return response
    
    def _format_context(self, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Format context chunks into a string for the prompt.
        
        Args:
            context_chunks: Retrieved context chunks
            
        Returns:
            Formatted context string
        """
        if not context_chunks:
            return "No relevant context found."
            
        formatted_chunks = []
        for i, chunk in enumerate(context_chunks):
            # Format each chunk with metadata
            title = chunk["metadata"].get("title", "Untitled")
            source = chunk["metadata"].get("source", "Unknown source")
            text = chunk["text"]
            
            formatted_chunk = f"[Document {i+1}] {title}\nSource: {source}\n\n{text}\n"
            formatted_chunks.append(formatted_chunk)
            
        return "\n".join(formatted_chunks)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create a prompt for the LLM.
        
        Args:
            query: User query
            context: Formatted context
            
        Returns:
            Complete prompt
        """
        return f"""You are a helpful AI assistant that answers questions based on the provided context.
        
CONTEXT:
{context}

USER QUERY:
{query}

Please answer the query based only on the provided context. If the context doesn't contain relevant information to answer the query, state that you don't have enough information to provide an answer. Include citations to specific documents when possible.

ANSWER:
"""
    
    def _call_llm_api(self, prompt: str) -> str:
        """
        Call the LLM API with the prompt.
        
        Args:
            prompt: Complete prompt
            
        Returns:
            Generated response
        """
        if not self.api_key:
            return "Error: API key not configured. Please set the OPENAI_API_KEY environment variable."
            
        try:
            # OpenAI API call
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error: API call failed with status code {response.status_code}. {response.text}"
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
