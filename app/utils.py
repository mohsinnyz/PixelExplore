from pathlib import Path
from PIL import Image


def save_thumbnail(src_path: str, dst_dir: str = "data/processed", size=(512, 512)) -> str:
    dst = Path(dst_dir)
    dst.mkdir(parents=True, exist_ok=True)
    out_path = dst / (Path(src_path).stem + "_thumb.jpg")
    with Image.open(src_path) as im:
        im.thumbnail(size)
        im.convert("RGB").save(out_path, "JPEG", quality=88)
    return str(out_path)