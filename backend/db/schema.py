"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MaterialMetadata(BaseModel):
    """Metadata for uploaded materials."""
    course: Optional[str] = None
    material_type: str  # lecture, textbook, notes, assignment, lab, exam
    lecture_number: Optional[int] = None
    chapter: Optional[str] = None
    topic: Optional[str] = None


class MaterialUploadResponse(BaseModel):
    """Response after uploading a material."""
    material_id: int
    filename: str
    chunk_count: int
    message: str


class MaterialListItem(BaseModel):
    """Item in the materials list."""
    id: int
    filename: str
    material_type: str
    course: Optional[str]
    upload_date: datetime
    chunk_count: int
    
    class Config:
        from_attributes = True


class QueryFilters(BaseModel):
    """Filters for query retrieval."""
    material_type: Optional[str] = None
    lecture_number: Optional[int] = None
    topic: Optional[str] = None
    material_ids: Optional[List[int]] = None


class SourceInfo(BaseModel):
    """Information about a source chunk."""
    chunk_id: str
    material_id: Optional[int] = None
    material_title: str
    page: Optional[int] = None
    section: Optional[str] = None
    material_type: str
    similarity_score: float


class QueryRequest(BaseModel):
    """Request for asking a question."""
    question: str = Field(..., min_length=3)
    filters: Optional[QueryFilters] = None
    top_k: Optional[int] = 12
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    """Response to a query."""
    answer: str
    sources: List[SourceInfo]
    faithfulness_score: Optional[float] = None
    verification_status: str  # passed, failed, warning, disabled
    confidence: float  # average similarity score


class ChunkDetail(BaseModel):
    """Detailed information about a chunk."""
    chunk_id: str
    text: str
    chunk_metadata: Dict[str, Any]
    material_id: int


class ReindexResponse(BaseModel):
    """Response after reindexing."""
    message: str
    chunks_indexed: int
    materials_processed: int


# Chat Schemas
class ChatSessionCreate(BaseModel):
    title: Optional[str] = None

class ChatSession(BaseModel):
    id: str  # UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    sources: Optional[List[SourceInfo]] = None
    verification_result: Optional[Dict] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ChatHistory(BaseModel):
    messages: List[ChatMessage]

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    filters: Optional[Dict] = None
