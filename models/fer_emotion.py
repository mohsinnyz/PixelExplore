# D:\pixelexplore\models\fer_emotion.py
from fer import FER
import numpy as np

class FEREmotion:
    def __init__(self):
        self.detector = FER(mtcnn=True)

    def analyze(self, image):
        results = self.detector.detect_emotions(np.array(image))
        if not results:
            return []
        emotions = results[0]["emotions"]
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        return [sorted_emotions[0][0]]  # return top emotion
