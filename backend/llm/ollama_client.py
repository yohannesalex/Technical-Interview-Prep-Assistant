"""
Ollama client for LLM integration.
Supports both local Ollama and remote Ollama API endpoints.
"""
import ollama
from typing import Optional, Dict, Any
import sys
sys.path.append('..')
from config import OLLAMA_MODEL, OLLAMA_URL, OLLAMA_API_KEY, LLM_TEMPERATURE, LLM_MAX_TOKENS


class OllamaClient:
    """Client for interacting with Ollama LLM (local or remote API)."""
    
    def __init__(
        self,
        model: str = OLLAMA_MODEL,
        base_url: str = OLLAMA_URL,
        api_key: Optional[str] = OLLAMA_API_KEY,
        temperature: float = LLM_TEMPERATURE
    ):
        """
        Initialize Ollama client.
        
        Args:
            model: Model name (e.g., mistral:7b-instruct)
            base_url: Ollama API URL (local or remote)
            api_key: Optional API key for authentication
            temperature: Sampling temperature
        """
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.temperature = temperature
        
        # Initialize client with optional authentication
        if api_key:
            # For APIs that require authentication, add headers
            self.client = ollama.Client(
                host=base_url,
                headers={'Authorization': f'Bearer {api_key}'}
            )
        else:
            self.client = ollama.Client(host=base_url)
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = LLM_MAX_TOKENS
    ) -> str:
        """
        Generate response from LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for instructions
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        
        messages.append({
            'role': 'user',
            'content': prompt
        })
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': self.temperature,
                    'num_predict': max_tokens
                }
            )
            
            return response['message']['content']
        
        except Exception as e:
            print(f"Error generating response: {e}")
            raise
    
    def check_availability(self) -> bool:
        """Check if Ollama is available and model is loaded."""
        try:
            self.client.list()
            return True
        except Exception as e:
            print(f"Ollama not available: {e}")
            return False


# Global client instance
_ollama_client = None


def get_ollama_client() -> OllamaClient:
    """Get or create the global Ollama client instance."""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client
