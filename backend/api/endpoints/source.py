"""
/source endpoint - Retrieve specific chunk details.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append('../..')
from db import get_db, crud, schema

router = APIRouter()


@router.get("/source/{chunk_id}", response_model=schema.ChunkDetail)
async def get_source(chunk_id: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific chunk.
    
    Args:
        chunk_id: Chunk ID
        db: Database session
        
    Returns:
        Chunk details with full metadata
    """
    chunk = crud.get_chunk(db, chunk_id)
    
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")
    
    return schema.ChunkDetail(
        chunk_id=chunk.chunk_id,
        text=chunk.text,
        chunk_metadata=chunk.chunk_metadata,
        material_id=chunk.material_id
    )
