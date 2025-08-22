from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from .services import description_builder, search_engine
from ..db.vector_store import vector_store
from pathlib import Path

router = APIRouter()

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
        # Save the uploaded file temporarily
        upload_path = UPLOAD_DIR / file.filename
        with open(upload_path, "wb") as f:
            f.write(await file.read())

        # Process the image to get a rich description and a unique ID
        # The description_builder service will handle all the model inference
        image_id, rich_description = description_builder.process_and_describe_image(upload_path)
        
        # Save the processed image with its unique ID in the processed directory
        processed_path = PROCESSED_DIR / f"{image_id}{upload_path.suffix}"
        upload_path.rename(processed_path)

        # Embed the description and add to the vector store
        vector_store.add_entry(image_id, rich_description)

        return {"status": "ok", "image_id": image_id, "description": rich_description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload and processing failed: {e}")

@router.post("/search-text/")
async def search_text(query: str = Form(...), top_k: int = Form(3)):
    """
    Performs a semantic search based on a text query.
    """
    try:
        results = search_engine.search_by_text(query, top_k=top_k)
        return JSONResponse({"query": query, "results": results})
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

        results = search_engine.search_by_image(query_path, top_k=top_k)
        
        # Clean up the temporary query image
        query_path.unlink()
        
        return JSONResponse({"results": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image search failed: {e}")