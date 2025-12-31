import requests
from typing import List
from src.core.config import settings

class LLMService:
    def __init__(self):
        # Use the variable from config
        self.ollama_api_url = settings.OLLAMA_BASE_URL 
        self.model = "llama3"

    def generate_response(self, query: str, context_chunks: List[dict]) -> str:
        """
        1. Joins the retrieved documents into a single context string.
        2. Sends a prompt to Llama 3.
        3. Returns the answer.
        """
        
        # Combine the text from all retrieved chunks
        context_text = "\n\n".join([chunk['content'] for chunk in context_chunks])
        
        # The Prompt Engineering part
        prompt = f"""
        You are a helpful expert assistant. Use the following context to answer the user's question.
        
        Context:
        {context_text}
        
        Question: 
        {query}
        
        If the answer is not in the context, just say "I don't know based on the provided documents."
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False  # We want the whole answer at once
        }

        try:
            response = requests.post(self.ollama_api_url, json=payload)
            response.raise_for_status()
            # Ollama returns a JSON object with a 'response' field
            return response.json().get("response", "")
        except Exception as e:
            return f"Error connecting to Llama 3: {str(e)}"