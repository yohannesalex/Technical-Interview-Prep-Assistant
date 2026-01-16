"""
Text chunking with section-awareness and configurable parameters.
"""
import tiktoken
from typing import List, Dict
import sys
sys.path.append('..')
from config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNK_MIN_SIZE


class TextChunker:
    """Intelligent text chunking with overlap and section awareness."""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Target chunk size in tokens
            overlap: Overlap size in tokens
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Chunk text into overlapping segments.
        
        Args:
            text: Text to chunk
            metadata: Base metadata to include in each chunk
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        if not text or not text.strip():
            return []
        
        metadata = metadata or {}
        
        # Split into sentences for better chunking
        sentences = self._split_sentences(text)
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)
            
            # If single sentence exceeds chunk size, split it
            if sentence_tokens > self.chunk_size:
                # Save current chunk if exists
                if current_chunk:
                    chunks.append({
                        'text': ' '.join(current_chunk),
                        'metadata': metadata.copy()
                    })
                    current_chunk = []
                    current_tokens = 0
                
                # Split long sentence by words
                words = sentence.split()
                temp_chunk = []
                temp_tokens = 0
                
                for word in words:
                    word_tokens = self.count_tokens(word + ' ')
                    if temp_tokens + word_tokens > self.chunk_size and temp_chunk:
                        chunks.append({
                            'text': ' '.join(temp_chunk),
                            'metadata': metadata.copy()
                        })
                        # Keep overlap
                        overlap_words = self._get_overlap_words(temp_chunk)
                        temp_chunk = overlap_words
                        temp_tokens = self.count_tokens(' '.join(temp_chunk))
                    
                    temp_chunk.append(word)
                    temp_tokens += word_tokens
                
                if temp_chunk:
                    current_chunk = temp_chunk
                    current_tokens = temp_tokens
                continue
            
            # Check if adding sentence exceeds chunk size
            if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append({
                    'text': ' '.join(current_chunk),
                    'metadata': metadata.copy()
                })
                
                # Start new chunk with overlap
                overlap_sentences = self._get_overlap_sentences(current_chunk)
                current_chunk = overlap_sentences + [sentence]
                current_tokens = self.count_tokens(' '.join(current_chunk))
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
        
        # Add final chunk
        if current_chunk and self.count_tokens(' '.join(current_chunk)) >= CHUNK_MIN_SIZE:
            chunks.append({
                'text': ' '.join(current_chunk),
                'metadata': metadata.copy()
            })
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_overlap_sentences(self, sentences: List[str]) -> List[str]:
        """Get sentences for overlap."""
        overlap_text = ' '.join(sentences)
        overlap_tokens = self.count_tokens(overlap_text)
        
        # Take sentences from the end until we reach overlap size
        result = []
        tokens = 0
        
        for sentence in reversed(sentences):
            sentence_tokens = self.count_tokens(sentence)
            if tokens + sentence_tokens > self.overlap:
                break
            result.insert(0, sentence)
            tokens += sentence_tokens
        
        return result
    
    def _get_overlap_words(self, words: List[str]) -> List[str]:
        """Get words for overlap."""
        result = []
        tokens = 0
        
        for word in reversed(words):
            word_tokens = self.count_tokens(word + ' ')
            if tokens + word_tokens > self.overlap:
                break
            result.insert(0, word)
            tokens += word_tokens
        
        return result
    
    def chunk_document_sections(self, sections: List[Dict]) -> List[Dict]:
        """
        Chunk document sections while preserving section metadata.
        
        Args:
            sections: List of section dicts from parser
            
        Returns:
            List of chunk dictionaries
        """
        all_chunks = []
        
        for section in sections:
            text = section.get('text', '')
            metadata = section.get('metadata', {})
            
            chunks = self.chunk_text(text, metadata)
            all_chunks.extend(chunks)
        
        return all_chunks
