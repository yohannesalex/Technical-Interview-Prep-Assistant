"""
/files endpoint - Serve material files for viewing.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import sys
sys.path.append('../..')
from db import get_db, crud

router = APIRouter()


@router.get("/files/{material_id}")
async def get_file(
    material_id: int,
    db: Session = Depends(get_db)
):
    """
    Serve the raw file for a material.
    Returns:
        FileResponse with appropriate media type.
    """
    material = crud.get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    if not os.path.exists(material.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
        
    return FileResponse(
        path=material.file_path,
        filename=material.filename,
        media_type="application/pdf" if material.filename.lower().endswith(".pdf") else "text/plain",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )
