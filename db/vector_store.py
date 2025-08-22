import faiss
import numpy as np
from transformers import CLIPTokenizer, CLIPModel
import torch
from typing import List, Dict


class VectorStore:
    def __init__(self):
        # Load CLIP text model (512d features for vit-base-patch32)
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
        self.dim = 512
        # Cosine similarity via inner product on normalized vectors
        self.index = faiss.IndexFlatIP(self.dim)
        self.data: List[Dict] = []  # list of {"desc", "path"}

    def _embed_text(self, text: str) -> np.ndarray:
        inputs = self.tokenizer([text], return_tensors="pt", padding=True)
        with torch.no_grad():
            feat = self.model.get_text_features(**inputs)
            feat = torch.nn.functional.normalize(feat, p=2, dim=1)
        return feat[0].cpu().numpy().astype("float32")

    def add_entry(self, image_path: str, desc: str):
        vec = self._embed_text(desc)[None, :]  # shape (1, d)
        self.index.add(vec)
        self.data.append({"desc": desc, "path": image_path})

    def search(self, query_text: str, top_k: int = 3):
        if len(self.data) == 0:
            return []
        q = self._embed_text(query_text)[None, :]
        sims, idxs = self.index.search(q, top_k)
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