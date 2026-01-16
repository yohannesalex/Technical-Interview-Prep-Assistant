"""
Embedding generation using SentenceTransformers.
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import sys
sys.path.append('..')
from config import EMBEDDING_MODEL, BATCH_SIZE


class Embedder:
    """Generate embeddings for text using SentenceTransformers."""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        Initialize embedder with specified model.
        
        Args:
            model_name: Name of the SentenceTransformers model
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.dimension}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Normalized embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        # L2 normalization for cosine similarity
        embedding = embedding / np.linalg.norm(embedding)
        return embedding
    
    def embed_batch(self, texts: List[str], show_progress: bool = True) -> np.ndarray:
        """
        Generate embeddings for a batch of texts.
        
        Args:
            texts: List of texts to embed
            show_progress: Whether to show progress bar
            
        Returns:
            Array of normalized embeddings
        """
        embeddings = self.model.encode(
            texts,
            batch_size=BATCH_SIZE,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        # L2 normalization for cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / norms
        
        return embeddings
    
    def get_dimension(self) -> int:
        """Get the dimension of embeddings."""
        return self.dimension


# Global embedder instance (singleton pattern)
_embedder_instance = None


def get_embedder() -> Embedder:
    """Get or create the global embedder instance."""
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = Embedder()
    return _embedder_instance
