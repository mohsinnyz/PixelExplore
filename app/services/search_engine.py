# D:\pixelexplore\app\services\search_engine.py

from db.vector_store import vector_store
from app.services.description_builder import DescriptionBuilder
from app.services.utils import load_image
from PIL import Image

class SearchEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.description_builder = DescriptionBuilder()

    def search_by_text(self, query: str, top_k: int = 3):
        """
        Performs a text-to-image semantic search.
        """
        return self.vector_store.search_by_text(query, top_k=top_k)

    def search_by_image(self, image_path: str, top_k: int = 3):
        """
        Performs an image-to-image semantic search by first generating an image embedding.
        """
        try:
            # First, embed the image using CLIP's image encoder
            query_image = Image.open(image_path).convert("RGB")
            
            # Now, perform the search using the image embedding
            return self.vector_store.search_by_image(query_image, top_k=top_k)
        except Exception as e:
            # Fallback to text search if image embedding fails
            print(f"Image search failed: {e}. Falling back to text search.")
            description = self.description_builder.build_description(image_path)['description']
            return self.vector_store.search_by_text(description, top_k=top_k)