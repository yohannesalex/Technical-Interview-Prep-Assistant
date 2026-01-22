"""
/admin endpoints - Administrative functions.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append('../..')
from db import get_db, crud, schema
from retrieval import get_embedder, get_vector_store
from ingestion import TextChunker

router = APIRouter()


@router.post("/admin/reindex", response_model=schema.ReindexResponse)
async def reindex(db: Session = Depends(get_db)):
    """
    Rebuild the vector index from all chunks in the database.
    
    Note: This is useful for manual index repairs or corruption recovery.
    
    Args:
        db: Database session
        
    Returns:
        Reindex response with statistics
    """
    try:
        all_chunks = db.query(crud.models.Chunk).all()
        
        if not all_chunks:
            # If no chunks in DB, clear the vector store
            vector_store = get_vector_store()
            vector_store.clear()
            vector_store.save()
            
            return schema.ReindexResponse(
                message="Database is empty. Index cleared.",
                chunks_indexed=0,
                materials_processed=0
            )
        
        vector_store = get_vector_store()
        vector_store.clear()
        
        embedder = get_embedder()
        chunk_texts = [chunk.text for chunk in all_chunks]
        chunk_ids = [chunk.chunk_id for chunk in all_chunks]
        
        print(f"Generating embeddings for {len(all_chunks)} chunks...")
        embeddings = embedder.embed_batch(chunk_texts)
        
        print(f"Adding to vector store...")
        vector_store.add_embeddings(embeddings, chunk_ids)
        
        vector_store.save()
        
        materials = db.query(crud.models.Material).all()
        
        return schema.ReindexResponse(
            message=f"Successfully reindexed {len(all_chunks)} chunks from {len(materials)} materials",
            chunks_indexed=len(all_chunks),
            materials_processed=len(materials)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reindexing: {str(e)}")


@router.post("/admin/reset")
async def reset_database(db: Session = Depends(get_db)):
    """
    Hard reset: Wipes ALL data and clears the index.
    """
    try:
        # Delete all tables content
        db.query(crud.models.ChatMessage).delete()
        db.query(crud.models.ChatSession).delete()
        db.query(crud.models.QueryLog).delete()
        db.query(crud.models.Chunk).delete()
        db.query(crud.models.Material).delete()
        db.commit()
        
        # Clear (empty) the vector store
        vector_store = get_vector_store()
        vector_store.clear()
        vector_store.save()
        
        return {"message": "System fully reset. All materials and history deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error resetting system: {str(e)}")
