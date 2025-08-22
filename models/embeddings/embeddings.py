# D:\pixelexplore\models\embeddings\embeddings.py

from sentence_transformers import SentenceTransformer
import numpy as np

class Embeddings:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the embeddings model.
        Default: all-MiniLM-L6-v2 (fast + good for semantic search).
        """
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        """
        Converts a single text description into a vector embedding.
        """
        return self.model.encode(text)

    def batch_encode(self, texts: list[str]) -> np.ndarray:
        """
        Converts a list of texts into embeddings in a batch.
        """
        return self.model.encode(texts, batch_size=32, show_progress_bar=False)