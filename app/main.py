# D:\pixelexplore\app\main.py
from fastapi import FastAPI
from .routes import router


app = FastAPI(title="Image Semantic Search")


# Mount routes
app.include_router(router)


@app.get("/")
def root():
    return {"message": "🚀 Image Semantic Search API is running"}