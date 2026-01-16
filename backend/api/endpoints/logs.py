"""
/logs endpoint - Query log retrieval.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append('../..')
from db import get_db, crud

router = APIRouter()


@router.get("/logs/{log_id}")
async def get_log(log_id: int, db: Session = Depends(get_db)):
    """
    Get a query log by ID.
    
    Args:
        log_id: Log ID
        db: Database session
        
    Returns:
        Query log details
    """
    log = crud.get_query_log(db, log_id)
    
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    return {
        "id": log.id,
        "timestamp": log.timestamp,
        "question": log.question,
        "answer": log.answer,
        "sources": log.sources,
        "faithfulness_score": log.faithfulness_score,
        "verification_status": log.verification_status,
        "filters_used": log.filters_used,
        "top_k": log.top_k
    }
