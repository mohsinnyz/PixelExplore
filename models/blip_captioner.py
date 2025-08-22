# D:\pixelexplore\models\blip_captioner.py
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

class BLIPCaptioner:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def generate(self, image: Image.Image) -> str:
        inputs = self.processor(image, return_tensors="pt")
        out = self.model.generate(**inputs, max_new_tokens=50)
        return self.processor.decode(out[0], skip_special_tokens=True)
