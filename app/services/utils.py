#D:\pixelexplore\app\services\utils.py
from pathlib import Path
from PIL import Image

def load_image(image_path: str) -> Image.Image:
    """Loads an image from a given path and converts it to RGB."""
    return Image.open(image_path).convert("RGB")

def save_thumbnail(src_path: str, dst_dir: str = "data/processed", size=(512, 512)) -> str:
    """
    Generates a thumbnail for an image and saves it.
    
    Args:
        src_path: The path to the source image.
        dst_dir: The destination directory for the thumbnail.
        size: The size of the thumbnail.
    
    Returns:
        The path to the saved thumbnail.
    """
    dst = Path(dst_dir)
    dst.mkdir(parents=True, exist_ok=True)
    out_path = dst / (Path(src_path).stem + "_thumb.jpg")
    with Image.open(src_path) as im:
        im.thumbnail(size)
        im.convert("RGB").save(out_path, "JPEG", quality=88)
    return str(out_path)