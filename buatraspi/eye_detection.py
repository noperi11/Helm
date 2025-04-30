import cv2
import numpy as np
from tensorflow.keras.models import load_model

class EyeDetector:
    def __init__(self,
                 model_path='eye_state_cnn.h5',
                 image_size=(48, 48),
                 roi_params=(0.4, 0.25, 0.5, 0.5),
                 threshold=0.99998):
        self.model = load_model(model_path)
        self.image_size = image_size
        self.xp, self.yp, self.wp, self.hp = roi_params
        self.threshold = threshold

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        x1 = int(w * self.xp)
        y1 = int(h * self.yp)
        x2 = int(x1 + w * self.wp)
        y2 = int(y1 + h * self.hp)
        roi = gray[y1:y2, x1:x2]
        roi_resized = cv2.resize(roi, self.image_size) / 255.0
        x = roi_resized.reshape(1, *self.image_size, 1)
        p = self.model.predict(x)[0][0]
        is_open = p > self.threshold
        return is_open, p, (x1, y1, x2, y2)

