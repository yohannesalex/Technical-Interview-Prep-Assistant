"""
FastAPI main application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
sys.path.append('..')
from config import CORS_ORIGINS, RERANK_ENABLED
from db import init_db
from retrieval import get_embedder, get_vector_store, get_reranker
from api.endpoints import ask, materials, source, logs, admin, chat, files
from retrieval import get_vector_store
from llm import get_ollama_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    print("Initializing database...")
    init_db()
    print("Database initialized")
    
    # Preload models
    print("Preloading retrieval models...")
    get_embedder()
    get_vector_store()
    if RERANK_ENABLED:
        get_reranker()
    print("Models loaded")
    
    yield
    
    print("Shutting down...")


app = FastAPI(
    title="RAG Interview Assistant API",
    description="API for checking answers against course materials locally.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask.router, tags=["Q&A"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(materials.router, tags=["Materials"])
app.include_router(source.router, tags=["Source"])
app.include_router(logs.router, tags=["Logs"])
app.include_router(admin.router, tags=["Admin"])
app.include_router(files.router, tags=["Files"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Technical Interview Prep Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "ask": "POST /ask - Ask a question",
            "materials": "GET /materials - List materials",
            "ingest": "POST /ingest - Upload material",
            "source": "GET /source/{chunk_id} - Get chunk details",
            "logs": "GET /logs/{log_id} - Get query log",
            "reindex": "POST /admin/reindex - Rebuild index"
        }
    }


@app.get("/health")
async def health():
    
    vector_store = get_vector_store()
    ollama = get_ollama_client()
    
    return {
        "status": "healthy",
        "vector_store_size": vector_store.get_size(),
        "ollama_available": ollama.check_availability()
    }
