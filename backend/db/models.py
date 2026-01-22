"""
Database models and setup for the RAG Interview Assistant.
Uses SQLAlchemy for ORM and SQLite for local storage.
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
from config import DATABASE_URL

sys.path.append('..')

Base = declarative_base()


class Material(Base):
    """Stores metadata about uploaded course materials."""
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    material_type = Column(String, nullable=False)  # lecture, textbook, notes, etc.
    course = Column(String, nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    chunk_count = Column(Integer, default=0)
    file_path = Column(String, nullable=False)
    

class Chunk(Base):
    """Stores individual text chunks with metadata."""
    __tablename__ = "chunks"
    
    chunk_id = Column(String, primary_key=True, index=True)  # UUID
    material_id = Column(Integer, nullable=False)
    embedding_id = Column(Integer, nullable=False)  # index in FAISS
    chunk_metadata = Column(JSON, nullable=False)  # full metadata schema
    text = Column(Text, nullable=False)
    

class ChatSession(Base):
    """Stores chat session metadata."""
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, index=True)  # UUID
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

class ChatMessage(Base):
    """Stores individual chat messages."""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)  # list of source chunks for assistant messages
    verification_result = Column(JSON, nullable=True)  # verification details
    timestamp = Column(DateTime, default=datetime.utcnow)


class QueryLog(Base):
    """Logs all queries for evaluation and debugging."""
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    sources = Column(JSON, nullable=True)  # list of source chunks
    faithfulness_score = Column(Float, nullable=True)
    verification_status = Column(String, nullable=True)  # passed, failed, warning
    filters_used = Column(JSON, nullable=True)
    top_k = Column(Integer, nullable=True)
    session_id = Column(String, nullable=True)  # Link to chat session


# Database engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
