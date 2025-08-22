from db.vector_store import vector_store
from . import description_builder


def search_by_text(query: str, top_k: int = 3):
    """Semantic search using text query."""
    return vector_store.search(query, top_k=top_k)


def search_by_image(image_path: str, top_k: int = 3):
    """Image-to-image semantic search by first generating a description (stub)."""
    desc = description_builder.build_description(image_path)
    return vector_store.search(desc, top_k=top_k)