"""
Optional cross-encoder reranking for improved precision.
"""
from sentence_transformers import CrossEncoder
from typing import List, Tuple
import sys
sys.path.append('..')
from config import RERANK_ENABLED


class Reranker:
    """Rerank retrieved chunks using cross-encoder."""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """
        Initialize reranker.
        
        Args:
            model_name: Name of the cross-encoder model
        """
        if RERANK_ENABLED:
            print(f"Loading reranker model: {model_name}")
            self.model = CrossEncoder(model_name)
            self.enabled = True
        else:
            self.model = None
            self.enabled = False
    
    def rerank(
        self,
        query: str,
        chunks: List[Tuple[str, str, float]]
    ) -> List[Tuple[str, str, float]]:
        """
        Rerank chunks based on query.
        
        Args:
            query: Query text
            chunks: List of (chunk_id, text, score) tuples
            
        Returns:
            Reranked list of (chunk_id, text, score) tuples
        """
        if not self.enabled or not chunks:
            return chunks
        
        # Prepare pairs for cross-encoder
        pairs = [[query, text] for _, text, _ in chunks]
        
        # Get reranking scores
        scores = self.model.predict(pairs)
        
        # Combine with original data and sort
        reranked = [
            (chunk_id, text, float(score))
            for (chunk_id, text, _), score in zip(chunks, scores)
        ]
        reranked.sort(key=lambda x: x[2], reverse=True)
        
        return reranked


# Global reranker instance
_reranker_instance = None


def get_reranker() -> Reranker:
    """Get or create the global reranker instance."""
    global _reranker_instance
    if _reranker_instance is None:
        _reranker_instance = Reranker()
    return _reranker_instance
