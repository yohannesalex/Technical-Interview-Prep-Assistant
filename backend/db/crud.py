"""
CRUD operations for database interactions.
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from . import models, schema


def create_material(
    db: Session,
    filename: str,
    material_type: str,
    file_path: str,
    course: Optional[str] = None
) -> models.Material:
    """Create a new material entry."""
    material = models.Material(
        filename=filename,
        material_type=material_type,
        file_path=file_path,
        course=course,
        upload_date=datetime.utcnow()
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


def get_material(db: Session, material_id: int) -> Optional[models.Material]:
    """Get a material by ID."""
    return db.query(models.Material).filter(models.Material.id == material_id).first()


def get_all_materials(db: Session) -> List[models.Material]:
    """Get all materials."""
    return db.query(models.Material).all()


def update_material_chunk_count(db: Session, material_id: int, chunk_count: int):
    """Update the chunk count for a material."""
    material = get_material(db, material_id)
    if material:
        material.chunk_count = chunk_count
        db.commit()


def delete_material(db: Session, material_id: int):
    """Delete a material and its chunks."""
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if material:
        # Delete chunks first
        db.query(models.Chunk).filter(models.Chunk.material_id == material_id).delete()
        # Delete material
        db.delete(material)
        db.commit()
    return material


def create_chunk(db: Session, chunk_id: str, material_id: int, embedding_id: int, chunk_metadata: Dict, text: str):
    """Create a new chunk."""
    db_chunk = models.Chunk(
        chunk_id=chunk_id,
        material_id=material_id,
        embedding_id=embedding_id,
        chunk_metadata=chunk_metadata,
        text=text
    )
    db.add(db_chunk)
    db.commit()
    db.refresh(db_chunk)
    return db_chunk


def get_chunk(db: Session, chunk_id: str) -> Optional[models.Chunk]:
    """Get a chunk by ID."""
    return db.query(models.Chunk).filter(models.Chunk.chunk_id == chunk_id).first()


def get_chunks_by_material(db: Session, material_id: int) -> List[models.Chunk]:
    """Get all chunks for a material."""
    return db.query(models.Chunk).filter(models.Chunk.material_id == material_id).all()


def create_query_log(
    db: Session,
    question: str,
    answer: str,
    sources: List[Dict],
    faithfulness_score: Optional[float],
    verification_status: str,
    filters_used: Dict,
    top_k: int,
    session_id: Optional[str] = None
) -> models.QueryLog:
    """Log a query."""
    db_log = models.QueryLog(
        question=question,
        answer=answer,
        sources=sources,
        faithfulness_score=faithfulness_score,
        verification_status=verification_status,
        filters_used=filters_used,
        top_k=top_k,
        session_id=session_id
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


# Chat CRUD
def create_chat_session(db: Session, title: Optional[str] = None) -> models.ChatSession:
    """Create a new chat session."""
    import uuid
    session_id = str(uuid.uuid4())
    db_session = models.ChatSession(
        id=session_id,
        title=title or f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_chat_sessions(db: Session, skip: int = 0, limit: int = 100) -> List[models.ChatSession]:
    """List chat sessions."""
    return db.query(models.ChatSession).order_by(models.ChatSession.updated_at.desc()).offset(skip).limit(limit).all()

def get_chat_session(db: Session, session_id: str) -> Optional[models.ChatSession]:
    """Get a chat session by ID."""
    return db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()

def update_chat_session_title(db: Session, session_id: str, title: str) -> Optional[models.ChatSession]:
    """Update session title."""
    db_session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if db_session:
        db_session.title = title
        db.commit()
        db.refresh(db_session)
    return db_session

def create_chat_message(
    db: Session,
    session_id: str,
    role: str,
    content: str,
    sources: Optional[List[Dict]] = None,
    verification_result: Optional[Dict] = None
) -> models.ChatMessage:
    """Add a message to a session."""
    db_message = models.ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        sources=sources,
        verification_result=verification_result
    )
    db.add(db_message)
    # Update session updated_at
    db_session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if db_session:
        db_session.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_message)
    return db_message

def get_chat_history(db: Session, session_id: str) -> List[models.ChatMessage]:
    """Get message history for a session."""
    return db.query(models.ChatMessage).filter(models.ChatMessage.session_id == session_id).order_by(models.ChatMessage.timestamp.asc()).all()


def get_recent_chat_history(db: Session, session_id: str, limit: int = 20) -> List[models.ChatMessage]:
    """Get the most recent messages for a session in chronological order."""
    messages = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.session_id == session_id)
        .order_by(models.ChatMessage.timestamp.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(messages))


def get_query_log(db: Session, log_id: int) -> Optional[models.QueryLog]:
    """Get a query log by ID."""
    return db.query(models.QueryLog).filter(models.QueryLog.id == log_id).first()
