"""
/chat endpoints - Session and message management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
import uuid
sys.path.append('../..')
from db import get_db, crud, schema
from typing import Optional

router = APIRouter()


@router.post("/chat/sessions", response_model=schema.ChatSession)
async def create_session(
    session: schema.ChatSessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new chat session."""
    return crud.create_chat_session(db, session.title)


@router.get("/chat/sessions", response_model=List[schema.ChatSession])
async def list_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List chat sessions."""
    return crud.get_chat_sessions(db, skip, limit)


@router.get("/chat/sessions/{session_id}", response_model=schema.ChatSession)
async def get_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get specific session details."""
    session = crud.get_chat_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/chat/sessions/{session_id}/history", response_model=List[schema.ChatMessage])
async def get_session_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get message history for a session."""
    # Verify session exists
    session = crud.get_chat_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    return crud.get_chat_history(db, session_id)


@router.put("/chat/sessions/{session_id}", response_model=schema.ChatSession)
async def update_session_title(
    session_id: str,
    update: schema.ChatSessionCreate,
    db: Session = Depends(get_db)
):
    """Update session title."""
    if not update.title:
        raise HTTPException(status_code=400, detail="Title is required")
        
    session = crud.update_chat_session_title(db, session_id, update.title)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
