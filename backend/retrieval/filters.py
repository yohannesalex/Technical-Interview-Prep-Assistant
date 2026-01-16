"""
Metadata filtering for retrieval.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
import sys
sys.path.append('..')
from db import models


class MetadataFilter:
    """Filter chunks based on metadata criteria."""
    
    @staticmethod
    def filter_chunks(
        db: Session,
        chunk_ids: List[str],
        material_type: Optional[str] = None,
        lecture_number: Optional[int] = None,
        topic: Optional[str] = None,
        material_ids: Optional[List[int]] = None
    ) -> List[str]:
        """
        Filter chunk IDs based on metadata criteria.
        
        Args:
            db: Database session
            chunk_ids: List of chunk IDs to filter
            material_type: Filter by material type
            lecture_number: Filter by lecture number
            topic: Filter by topic (case-insensitive partial match)
            material_ids: Filter by specific material IDs
            
        Returns:
            Filtered list of chunk IDs
        """
        if not chunk_ids:
            return []
        
        # Get chunks from database
        filtered_ids = []
        for chunk_id in chunk_ids:
            chunk = db.query(models.Chunk).filter(models.Chunk.chunk_id == chunk_id).first()
            if not chunk:
                continue
            
            # Filter by material IDs if provided
            if material_ids is not None and chunk.material_id not in material_ids:
                continue

            metadata = chunk.chunk_metadata
            
            # Apply other filters
            if material_type and metadata.get('material_type') != material_type:
                continue
            
            if lecture_number is not None and metadata.get('lecture_number') != lecture_number:
                continue
            
            if topic:
                chunk_topic = metadata.get('topic', '').lower()
                if topic.lower() not in chunk_topic:
                    continue
            
            filtered_ids.append(chunk.chunk_id)
        
        return filtered_ids
    
    @staticmethod
    def apply_filters_to_results(
        db: Session,
        results: List[tuple],
        material_type: Optional[str] = None,
        lecture_number: Optional[int] = None,
        topic: Optional[str] = None,
        material_ids: Optional[List[int]] = None
    ) -> List[tuple]:
        """
        Apply filters to search results.
        
        Args:
            db: Database session
            results: List of (chunk_id, score) tuples
            material_type: Filter by material type
            lecture_number: Filter by lecture number
            topic: Filter by topic
            
        Returns:
            Filtered list of (chunk_id, score) tuples
        """
        if not results:
            return []
        
        chunk_ids = [chunk_id for chunk_id, _ in results]
        filtered_ids = MetadataFilter.filter_chunks(
            db, chunk_ids, material_type, lecture_number, topic, material_ids
        )
        
        # Keep only filtered results, preserving scores
        filtered_results = [
            (chunk_id, score) for chunk_id, score in results
            if chunk_id in filtered_ids
        ]
        
        return filtered_results
