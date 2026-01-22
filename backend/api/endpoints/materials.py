"""
/materials and /ingest endpoints - Material management.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pathlib import Path
from typing import List, Optional
import shutil
import uuid
import sys
sys.path.append('../..')
from db import get_db, crud, schema
from ingestion import DocumentParser, TextChunker, MetadataExtractor
from retrieval import get_embedder, get_vector_store
from config import DATA_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from api.endpoints.admin import reindex

router = APIRouter()


@router.get("/materials", response_model=List[schema.MaterialListItem])
async def list_materials(db: Session = Depends(get_db)):
    """List all uploaded materials."""
    materials = crud.get_all_materials(db)
    return materials


@router.post("/ingest", response_model=schema.MaterialUploadResponse)
async def ingest_material(
    file: UploadFile = File(...),
    material_type: str = Form("document"),
    course: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload and process a new material.
    
    Args:
        file: Uploaded file
        material_type: Type of material (lecture, textbook, etc.)
        course: Course name
        db: Database session
        
    Returns:
        Upload response with material ID and chunk count
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Allowed: {ALLOWED_EXTENSIONS}"
            )
        
        # We've removed the strict check for config.MATERIAL_TYPES to allow simplified uploads
        if not material_type:
            material_type = "document"
        
        # Create material directory based on type
        material_dir = Path(DATA_DIR) / f"{material_type}s"  # lectures, textbooks, etc.
        material_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = material_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create material entry in database
        material = crud.create_material(
            db, file.filename, material_type, str(file_path), course
        )
        
        # Parse document
        print(f"Parsing {file.filename}...")
        sections = DocumentParser.parse(str(file_path))
        
        # Extract base metadata
        base_metadata = MetadataExtractor.extract_from_filename(
            file.filename, material_type, course
        )
        base_metadata['material_file'] = str(file_path)
        
        # Chunk document
        print(f"Chunking document...")
        chunker = TextChunker()
        all_chunks = []
        
        for section in sections:
            # Merge section metadata with base metadata
            section_metadata = MetadataExtractor.merge_metadata(
                base_metadata, section.get('metadata', {})
            )
            
            # Chunk the section
            chunks = chunker.chunk_text(section.get('text', ''), section_metadata)
            all_chunks.extend(chunks)
        
        print(f"Created {len(all_chunks)} chunks")
        
        # Generate embeddings
        print(f"Generating embeddings...")
        embedder = get_embedder()
        chunk_texts = [chunk['text'] for chunk in all_chunks]
        embeddings = embedder.embed_batch(chunk_texts)
        
        # Add to vector store
        print(f"Adding to vector store...")
        vector_store = get_vector_store()
        chunk_ids = [str(uuid.uuid4()) for _ in all_chunks]
        vector_store.add_embeddings(embeddings, chunk_ids)
        
        # Save chunks to database
        print(f"Saving chunks to database...")
        for i, (chunk, chunk_id) in enumerate(zip(all_chunks, chunk_ids)):
            # Create full metadata
            full_metadata = MetadataExtractor.create_chunk_metadata(
                chunk['metadata'],
                chunk['text']
            )
            full_metadata['chunk_id'] = chunk_id
            
            crud.create_chunk(
                db, chunk_id, material.id, i, full_metadata, chunk['text']
            )
        
        # Update material chunk count
        crud.update_material_chunk_count(db, material.id, len(all_chunks))
        
        # Save vector store
        vector_store.save()
        
        print(f"Successfully ingested {file.filename}")
        
        return schema.MaterialUploadResponse(
            material_id=material.id,
            filename=file.filename,
            chunk_count=len(all_chunks),
            message=f"Successfully processed {file.filename} into {len(all_chunks)} chunks"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.delete("/materials/{material_id}")
async def delete_material(material_id: int, db: Session = Depends(get_db)):
    """Delete a material and its chunks."""
    success = crud.delete_material(db, material_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Material not found")
    
    # Automatically reindex to remove vectors
    # This might be slow for large datasets, but ensures consistency
    await reindex(db)
    
    return {"message": "Material deleted and index updated."}
