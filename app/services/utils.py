#D:\pixelexplore\app\services\utils.py
from PIL import Image

def load_image(image_path: str) -> Image.Image:
    """Loads an image from a given path."""
    return Image.open(image_path).convert("RGB")