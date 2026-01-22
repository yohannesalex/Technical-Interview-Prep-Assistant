"""LLM package initialization."""
from .openrouter_client import OpenRouterClient, get_llm_client
from .prompts import SYSTEM_PROMPT, create_rag_prompt, extract_refusal_keywords
from .formatter import AnswerFormatter

# Backward compatibility alias
get_ollama_client = get_llm_client

__all__ = [
    "OpenRouterClient", 
    "get_llm_client", 
    "get_ollama_client",  # Alias for backward compatibility
    "SYSTEM_PROMPT", 
    "create_rag_prompt", 
    "extract_refusal_keywords",
    "AnswerFormatter"
]
