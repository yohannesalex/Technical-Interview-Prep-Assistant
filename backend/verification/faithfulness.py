"""
Faithfulness verification - check if answer is supported by retrieved chunks.
"""
import re
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
import sys
sys.path.append('..')
from config import EMBEDDING_MODEL


class FaithfulnessChecker:
    """Check if generated answer is faithful to retrieved context."""
    
    def __init__(self):
        """Initialize with embedding model for semantic similarity."""
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.similarity_threshold = 0.5  # Threshold for considering a sentence supported
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Remove citations first
        text = re.sub(r'\[([^\]]+)\]', '', text)
        
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        return sentences
    
    def check_sentence_support(
        self,
        sentence: str,
        context_chunks: List[str]
    ) -> Tuple[bool, float]:
        """
        Check if a sentence is supported by context.
        
        Args:
            sentence: Sentence to check
            context_chunks: List of context texts
            
        Returns:
            Tuple of (is_supported, max_similarity)
        """
        if not context_chunks:
            return False, 0.0
        
        # Embed sentence and contexts
        sentence_emb = self.model.encode(sentence, convert_to_numpy=True)
        context_embs = self.model.encode(context_chunks, convert_to_numpy=True)
        
        # Compute cosine similarities
        sentence_emb = sentence_emb / np.linalg.norm(sentence_emb)
        context_embs = context_embs / np.linalg.norm(context_embs, axis=1, keepdims=True)
        
        similarities = np.dot(context_embs, sentence_emb)
        max_similarity = float(np.max(similarities))
        
        is_supported = max_similarity >= self.similarity_threshold
        
        return is_supported, max_similarity
    
    def verify_answer(
        self,
        answer: str,
        context_chunks: List[Dict]
    ) -> Dict:
        """
        Verify answer faithfulness.
        
        Args:
            answer: Generated answer
            context_chunks: List of context chunk dictionaries
            
        Returns:
            Verification report dictionary
        """
        # Extract just the text from chunks
        context_texts = [chunk.get('text', '') for chunk in context_chunks]
        
        # Split answer into sentences
        sentences = self.split_into_sentences(answer)
        
        if not sentences:
            return {
                'faithfulness_score': 1.0,
                'total_sentences': 0,
                'supported_sentences': 0,
                'unsupported_sentences': [],
                'sentence_details': []
            }
        
        # Check each sentence
        sentence_details = []
        supported_count = 0
        
        for sentence in sentences:
            is_supported, similarity = self.check_sentence_support(sentence, context_texts)
            
            sentence_details.append({
                'sentence': sentence,
                'supported': is_supported,
                'max_similarity': similarity
            })
            
            if is_supported:
                supported_count += 1
        
        # Calculate faithfulness score
        faithfulness_score = supported_count / len(sentences) if sentences else 1.0
        
        # Get unsupported sentences
        unsupported = [
            detail['sentence'] for detail in sentence_details
            if not detail['supported']
        ]
        
        return {
            'faithfulness_score': faithfulness_score,
            'total_sentences': len(sentences),
            'supported_sentences': supported_count,
            'unsupported_sentences': unsupported,
            'sentence_details': sentence_details
        }


# Global checker instance
_faithfulness_checker = None


def get_faithfulness_checker() -> FaithfulnessChecker:
    """Get or create the global faithfulness checker instance."""
    global _faithfulness_checker
    if _faithfulness_checker is None:
        _faithfulness_checker = FaithfulnessChecker()
    return _faithfulness_checker
