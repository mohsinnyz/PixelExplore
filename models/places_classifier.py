# D:\pixelexplore\models\places_classifier.py
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import os

class PlacesClassifier:
    def __init__(self):
        self.model = models.resnet18(num_classes=365)
        model_file = "models/scenes/resnet18_places365.pth.tar"
        if not os.path.exists(model_file):
            os.makedirs("models/scenes", exist_ok=True)
            torch.hub.download_url_to_file(
                "http://places2.csail.mit.edu/models_places365/resnet18_places365.pth.tar",
                model_file
            )

        checkpoint = torch.load(model_file, map_location="cpu")
        state_dict = {str.replace(k, 'module.', ''): v for k, v in checkpoint['state_dict'].items()}
        self.model.load_state_dict(state_dict)
        self.model.eval()

        # categories
        category_file = "models/scenes/categories_places365.txt"
        if not os.path.exists(category_file):
            torch.hub.download_url_to_file(
                "https://raw.githubusercontent.com/CSAILVision/places365/master/categories_places365.txt",
                category_file
            )
        self.classes = [line.strip().split(' ')[0][3:] for line in open(category_file)]

        self.tf = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def classify(self, image_path: str) -> str:
        img = Image.open(image_path).convert("RGB")
        input_img = self.tf(img).unsqueeze(0)
        with torch.no_grad():
            logit = self.model(input_img)
        _, pred = logit.topk(1)
        return self.classes[pred.item()]


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