# D:\pixelexplore\app\services\query_parser.py

from typing import Dict, Any
import re

class QueryParser:
    """
    Parse user queries into structured form for semantic + filter-based search.
    """

    def __init__(self):
        # In future, you could replace with Llama 3 / Gemini API for richer parsing
        pass

    def parse(self, query: str) -> Dict[str, Any]:
        """
        Parse query string into tokens and potential filters.
        Example:
            "picture of me in white t shirt and black boots standing on a bridge"
        Returns:
            {
                "raw": "...",
                "keywords": [...],
                "filters": {
                    "color": ["white", "black"],
                    "objects": ["t shirt", "boots", "bridge"]
                }
            }
        """
        tokens = query.lower().split()
        filters = {}

        # Very naive color extraction
        colors = ["white", "black", "blue", "red", "green", "yellow"]
        found_colors = [c for c in colors if c in tokens]
        if found_colors:
            filters["color"] = found_colors

        # Very naive object extraction (just split by nouns in query for now)
        object_patterns = ["t shirt", "boots", "dog", "cat", "bridge", "car", "tree", "beach"]
        found_objects = [obj for obj in object_patterns if obj in query.lower()]
        if found_objects:
            filters["objects"] = found_objects

        return {
            "raw": query,
            "keywords": tokens,
            "filters": filters
        }


# Quick test
if __name__ == "__main__":
    parser = QueryParser()
    print(parser.parse("picture of me in white t shirt and black boots standing on a bridge"))
