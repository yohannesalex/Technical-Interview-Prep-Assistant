"""
OpenRouter LLM client for high-performance cloud models.
Replaces Ollama with OpenRouter API for better performance.
"""
import requests
from typing import Optional
import sys
sys.path.append('..')
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS


class OpenRouterClient:
    """Client for interacting with OpenRouter API."""
    
    def __init__(
        self,
        api_key: str = OPENROUTER_API_KEY,
        base_url: str = OPENROUTER_BASE_URL,
        model: str = OPENROUTER_MODEL,
        temperature: float = LLM_TEMPERATURE
    ):
        """
        Initialize OpenRouter client.
        
        Args:
            api_key: OpenRouter API key
            base_url: OpenRouter API base URL
            model: Model name (e.g., "anthropic/claude-3.5-sonnet")
            temperature: Sampling temperature
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        
        # Debug print masked key
        masked_key = f"{api_key[:10]}...{api_key[-5:]}" if api_key else "None"
        print(f"DEBUG: OpenRouterClient initialized with key: {masked_key}")
        
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",  # Optional: for rankings
            "X-Title": "Technical Interview Prep Assistant"  # Optional: for rankings
        }
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = LLM_MAX_TOKENS
    ) -> str:
        """
        Generate response from LLM via OpenRouter.
        
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
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": max_tokens
                },
                timeout=60  # 60 second timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data['choices'][0]['message']['content']
        
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenRouter API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
        except (KeyError, IndexError) as e:
            print(f"Error parsing OpenRouter response: {e}")
            raise
    
    def check_availability(self) -> bool:
        """Check if OpenRouter API is available."""
        try:
            # Simple test request
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"OpenRouter not available: {e}")
            return False


# Global client instance
_openrouter_client = None


def get_llm_client() -> OpenRouterClient:
    """Get or create the global OpenRouter client instance."""
    global _openrouter_client
    if _openrouter_client is None:
        _openrouter_client = OpenRouterClient()
    return _openrouter_client
