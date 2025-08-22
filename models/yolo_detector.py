#D:\pixelexplore\models\yolo_detector.py
from ultralytics import YOLO

class YOLODetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")  # lightweight version

    def detect(self, image_path: str):
        results = self.model(image_path)
        objects = []
        for r in results:
            objects.extend([self.model.names[int(cls)] for cls in r.boxes.cls])
        return list(set(objects))
