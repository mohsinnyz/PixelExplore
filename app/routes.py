# D:\pixelexplore\app\routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from db.vector_store import vector_store
from app.services.description_builder import DescriptionBuilder
from app.services.search_engine import SearchEngine
from app.services.utils import load_image, save_thumbnail
from pathlib import Path
import os
import uuid

router = APIRouter()

# Initialize services
description_builder = DescriptionBuilder()
search_engine = SearchEngine(vector_store)

# Directories for storing uploaded images and processed images
UPLOAD_DIR = Path("data/uploads")
PROCESSED_DIR = Path("data/processed")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """
    Uploads an image, processes it, and adds its description to the vector store.
    """
    try:
        # Save the uploaded file with a unique ID
        file_id = str(uuid.uuid4())
        file_ext = Path(file.filename).suffix
        upload_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        with open(upload_path, "wb") as f:
            f.write(await file.read())

        # Process the image to get a rich description
        rich_description = description_builder.build_description(str(upload_path))
        
        # Create and save a thumbnail
        thumbnail_path = save_thumbnail(str(upload_path))
        
        # Add the entry to the vector store.
        vector_store.add_entry(str(thumbnail_path), rich_description['description'])
        
        # Move the full-size image to the processed directory
        processed_path = PROCESSED_DIR / f"{file_id}{file_ext}"
        os.rename(upload_path, processed_path)

        return {"status": "ok", "description": rich_description['description'], "id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload and processing failed: {e}")

@router.post("/search-text/")
async def search_text(query: str = Form(...), top_k: int = Form(3)):
    """
    Performs a semantic search based on a text query.
    """
    try:
        results = search_engine.search_by_text(query, top_k=top_k)
        return JSONResponse(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text search failed: {e}")

@router.post("/search-image/")
async def search_image(file: UploadFile = File(...), top_k: int = Form(3)):
    """
    Performs a semantic search based on a query image.
    """
    try:
        # Save the query image temporarily
        query_path = UPLOAD_DIR / ("query_" + file.filename)
        with open(query_path, "wb") as f:
            f.write(await file.read())

        results = search_engine.search_by_image(str(query_path), top_k=top_k)
        
        # Clean up the temporary query image
        os.unlink(query_path)
        
        return JSONResponse(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image search failed: {e}")