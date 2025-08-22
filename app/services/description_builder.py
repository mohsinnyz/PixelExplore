# D:\pixelexplore\app\services\description_builder.py

from .models import BLIPCaptioner, YOLODetector, PlacesClassifier, FEREmotion
from .utils import load_image

class DescriptionBuilder:
    def __init__(self):
        self.captioner = BLIPCaptioner()
        self.detector = YOLODetector()
        self.places = PlacesClassifier()
        self.fer = FEREmotion()

    def build_description(self, image_path: str) -> dict:
        image = load_image(image_path)

        caption = self.captioner.generate(image)
        objects = self.detector.detect(image_path)
        scene = self.places.classify(image_path)
        emotions = self.fer.analyze(image)

        description = f"{caption}. Scene: {scene}. Objects: {', '.join(objects)}."
        if emotions:
            description += f" Detected emotions: {', '.join(emotions)}."

        return {
            "description": description,
            "caption": caption,
            "scene": scene,
            "objects": objects,
            "emotions": emotions
        }
