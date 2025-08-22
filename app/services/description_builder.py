# D:\pixelexplore\app\services\description_builder.py

from models.captioning.blip_captioner import BLIPCaptioner
from models.detection.yolo_detector import YOLODetector
from models.scenes.places_classifier import PlacesClassifier
from models.emotion.fer_emotion import FEREmotion
from app.services.utils import load_image

class DescriptionBuilder:
    def __init__(self):
        """
        Initializes all necessary models for image analysis.
        """
        self.captioner = BLIPCaptioner()
        self.detector = YOLODetector()
        self.places = PlacesClassifier()
        self.fer = FEREmotion()

    def build_description(self, image_path: str) -> dict:
        """
        Orchestrates the image analysis pipeline to create a rich description.

        Args:
            image_path: The file path to the image to be analyzed.

        Returns:
            A dictionary containing the fused description and its components.
        """
        image = load_image(image_path)

        caption = self.captioner.generate(image)
        objects = self.detector.detect(image_path)
        scene = self.places.classify(image_path)
        emotions = self.fer.analyze(image)

        description = f"{caption}. The scene is a {scene}."
        if objects:
            description += f" Objects detected include {', '.join(objects)}."
        if emotions:
            description += f" People in the image appear to be expressing {', '.join(emotions)}."

        return {
            "description": description,
            "caption": caption,
            "scene": scene,
            "objects": objects,
            "emotions": emotions
        }