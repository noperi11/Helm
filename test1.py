import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load your trained model
model = load_model('eye_state_cnn.h5')

# Settings
image_size = (48, 48)  # Must match your training size

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # For simplicity, we'll just take a center region assuming the eye is there
    h, w = gray.shape
    x1 = int(w*0.4)
    y1= int(h*0.25)
    x2 = int(x1 + w*0.5)
    y2=int(y1+h*0.5)

    roi = gray[y1:y2, x1:x2]  # Crop region of interest

    # Resize to model input size
    roi_resized = cv2.resize(roi, image_size)
    roi_resized = roi_resized / 255.0
    roi_resized = roi_resized.reshape(1, 48, 48, 1)

    # Predict
    prediction = model.predict(roi_resized)[0][0]
    label = "Open" if prediction >0.99998 else "Closed"

    # Draw bounding box
    color = (0, 255, 0) if label == "Open" else (0, 0, 255)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Put label text
    cv2.putText(frame, f'Eye: {label},{prediction}', (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Display
    cv2.imshow('Eye State Detection', frame)

    # Exit when 'q' pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

