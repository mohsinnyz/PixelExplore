from pathlib import Path

# TODO: Replace this stub with BLIP-2 + YOLO + Places + FER integration

def build_description(image_path: str) -> str:
    """Return a placeholder rich description for now.
    Later: generate caption + objects + scene + emotion and merge.
    """
    name = Path(image_path).stem.replace("_", " ")
    return f"Photo named '{name}'. (stub description to be replaced by models)"