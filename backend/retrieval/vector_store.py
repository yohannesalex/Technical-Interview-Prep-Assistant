"""
FAISS vector store for similarity search.
"""
import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import sys
sys.path.append('..')
from config import INDEX_DIR, EMBEDDING_DIMENSION


class VectorStore:
    """FAISS-based vector store for semantic search."""
    
    def __init__(self, dimension: int = EMBEDDING_DIMENSION):
        """
        Initialize vector store.
        
        Args:
            dimension: Dimension of embeddings
        """
        self.dimension = dimension
        # Use IndexFlatIP for exact cosine similarity (inner product with normalized vectors)
        self.index = faiss.IndexFlatIP(dimension)
        self.chunk_ids = []  # Maps index position to chunk_id
        self.index_dir = Path(INDEX_DIR)
        self.index_dir.mkdir(exist_ok=True)
    
    def add_embeddings(self, embeddings: np.ndarray, chunk_ids: List[str]):
        """
        Add embeddings to the index.
        
        Args:
            embeddings: Array of embeddings (N x dimension)
            chunk_ids: List of chunk IDs corresponding to embeddings
        """
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension mismatch: expected {self.dimension}, got {embeddings.shape[1]}")
        
        # Ensure embeddings are float32
        embeddings = embeddings.astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings)
        self.chunk_ids.extend(chunk_ids)
        
        print(f"Added {len(chunk_ids)} embeddings to index. Total: {self.index.ntotal}")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 12) -> List[Tuple[str, float]]:
        """
        Search for similar chunks.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of (chunk_id, similarity_score) tuples
        """
        if len(self.chunk_ids) == 0:
            return []
        
        # Ensure query is 2D and float32
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        query_embedding = query_embedding.astype('float32')
        
        # Search
        k = min(top_k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding, k)
        
        # Convert to results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunk_ids):  # Valid index
                chunk_id = self.chunk_ids[idx]
                similarity = float(dist)  # Already cosine similarity due to normalized vectors
                results.append((chunk_id, similarity))
        
        return results
    
    def save(self, name: str = "faiss"):
        """
        Save index and metadata to disk.
        
        Args:
            name: Name prefix for saved files
        """
        index_path = self.index_dir / f"{name}.index"
        metadata_path = self.index_dir / f"{name}_metadata.pkl"
        
        # Save FAISS index
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata
        metadata = {
            'chunk_ids': self.chunk_ids,
            'dimension': self.dimension
        }
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"Saved index to {index_path}")
    
    def load(self, name: str = "faiss") -> bool:
        """
        Load index and metadata from disk.
        
        Args:
            name: Name prefix for saved files
            
        Returns:
            True if loaded successfully, False otherwise
        """
        index_path = self.index_dir / f"{name}.index"
        metadata_path = self.index_dir / f"{name}_metadata.pkl"
        
        if not index_path.exists() or not metadata_path.exists():
            print("No saved index found")
            return False
        
        # Load FAISS index
        self.index = faiss.read_index(str(index_path))
        
        # Load metadata
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        self.chunk_ids = metadata['chunk_ids']
        self.dimension = metadata['dimension']
        
        print(f"Loaded index from {index_path}. Total vectors: {self.index.ntotal}")
        return True
    
    def clear(self):
        """Clear the index."""
        self.index = faiss.IndexFlatIP(self.dimension)
        self.chunk_ids = []
        print("Index cleared")
    
    def get_size(self) -> int:
        """Get the number of vectors in the index."""
        return self.index.ntotal


# Global vector store instance
_vector_store_instance = None


def get_vector_store() -> VectorStore:
    """Get or create the global vector store instance."""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
        # Try to load existing index
        _vector_store_instance.load()
    return _vector_store_instance
