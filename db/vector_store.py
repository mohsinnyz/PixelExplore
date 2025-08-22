# D:\pixelexplore\db\vector_store.py

import faiss
import numpy as np
from transformers import CLIPTokenizer, CLIPModel, CLIPProcessor
from PIL import Image
import torch
from typing import List, Dict

class VectorStore:
    def __init__(self):
        """
        Initializes the vector store with a pre-trained CLIP model
        and a FAISS index for efficient similarity search.
        """
        # Load CLIP model, tokenizer, and processor
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        self.dim = 512
        # Cosine similarity via inner product on normalized vectors
        self.index = faiss.IndexFlatIP(self.dim)
        self.data: List[Dict] = []  # list of {"desc", "path"}

    def _embed_text(self, text: str) -> np.ndarray:
        """Converts text into a vector embedding using CLIP."""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            feat = self.model.get_text_features(**inputs)
            feat = torch.nn.functional.normalize(feat, p=2, dim=1)
        return feat[0].cpu().numpy().astype("float32")

    def _embed_image(self, image: Image.Image) -> np.ndarray:
        """Converts a PIL Image into a vector embedding using CLIP."""
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            feat = self.model.get_image_features(**inputs)
            feat = torch.nn.functional.normalize(feat, p=2, dim=1)
        return feat[0].cpu().numpy().astype("float32")
        
    def add_entry(self, image_path: str, desc: str):
        """Adds a text-based entry to the vector store."""
        vec = self._embed_text(desc)[None, :]  # shape (1, d)
        self.index.add(vec)
        self.data.append({"desc": desc, "path": image_path})

    def search_by_text(self, query_text: str, top_k: int = 3) -> List[Dict]:
        """Performs a semantic search with a text query."""
        if len(self.data) == 0:
            return []
        q = self._embed_text(query_text)[None, :]
        return self._do_search(q, top_k)

    def search_by_image(self, query_image: Image.Image, top_k: int = 3) -> List[Dict]:
        """Performs a semantic search with an image query."""
        if len(self.data) == 0:
            return []
        q = self._embed_image(query_image)[None, :]
        return self._do_search(q, top_k)
        
    def _do_search(self, query_vec, top_k: int) -> List[Dict]:
        """Helper method to perform the FAISS search and format results."""
        sims, idxs = self.index.search(query_vec, top_k)
        results = []
        for i, s in zip(idxs[0], sims[0]):
            if i < 0 or i >= len(self.data):
                continue
            item = self.data[i]
            results.append({
                "path": item["path"],
                "desc": item["desc"],
                "score": float(s),
            })
        return results

# Singleton store
vector_store = VectorStore()