import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
from flask import Flask, Response
from gpiozero import Buzzer
import time

# Inisialisasi Flask
app = Flask(__name__)

# Inisialisasi Buzzer
buzzer = Buzzer(27)  # Sesuaikan dengan pin GPIO yang digunakan

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]
EYE_AR_THRESH = 0.26
EYE_CLOSED_TIME_THRESH = 2.0  # Waktu dalam detik

cap = cv2.VideoCapture(0)

eye_closed_start_time = None

def generate_frames():
    global eye_closed_start_time

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                left_eye = np.array([(int(landmarks[idx].x * w), int(landmarks[idx].y * h)) for idx in LEFT_EYE_IDX], dtype="float")
                right_eye = np.array([(int(landmarks[idx].x * w), int(landmarks[idx].y * h)) for idx in RIGHT_EYE_IDX], dtype="float")

                leftEAR = eye_aspect_ratio(left_eye)
                rightEAR = eye_aspect_ratio(right_eye)
                ear = (leftEAR + rightEAR) / 2.0

                if ear < EYE_AR_THRESH:
                    if eye_closed_start_time is None:
                        eye_closed_start_time = time.time()
                    elif time.time() - eye_closed_start_time >= EYE_CLOSED_TIME_THRESH:
                        buzzer.on()
                else:
                    eye_closed_start_time = None
                    buzzer.off()

                status = "Eyes Open" if ear >= EYE_AR_THRESH else "Eyes Closed"
                color = (0, 255, 0) if status == "Eyes Open" else (0, 0, 255)

                cv2.polylines(frame, [left_eye.astype(np.int32)], True, color, 1)
                cv2.polylines(frame, [right_eye.astype(np.int32)], True, color, 1)
                cv2.putText(frame, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(frame, f"EAR: {ear:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<html><body><h1>Eye State Detection</h1><img src='/video_feed' width='640'></body></html>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
