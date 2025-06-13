import cv2
import time
from threading import Thread
from gpiozero import LED, Buzzer, Button
from signal import pause
from eye_detection import EyeDetector
from mpu_sensor import HeadTilt
from alerts import AlertDevice

# --- Touch Sensor Setup ---
touch_sensor = Button(24, hold_time=5)  # 5 seconds hold time
program_started = False

# --- Initialize devices ---
alert = AlertDevice()

# --- Initialize detector and sensors ---
eye = EyeDetector()
head = HeadTilt(threshold_deg=6)
cap = cv2.VideoCapture(0)

eye_closed_start = None
eye_alerted = False

# --- Define function to run main logic ---
def run_detection():
    global eye_closed_start, eye_alerted

    print("Starting Smart Helmet Monitoring...")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            is_open, p, rect = eye.detect(frame)

            # Override by MPU6050
            if head.is_tilted():
                alert.start_override()
            else:
                alert.stop_override()

                # Eye detection logic
                if not is_open:
                    if eye_closed_start is None:
                        eye_closed_start = time.time()
                    elif not eye_alerted and time.time() - eye_closed_start >= 0.8:
                        print("Eyes closed - Alert activated")
                        alert.start_alert()
                        eye_alerted = True
                else:
                    eye_closed_start = None
                    eye_alerted = False

            # Optional - show video frame
            # color = (0,255,0) if is_open else (0,0,255)
            # x1,y1,x2,y2 = rect
            # cv2.rectangle(frame, (x1,y1),(x2,y2), color, 2)
            # cv2.imshow('Smart Helm', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    finally:
        cap.release()
        # cv2.destroyAllWindows()

# --- Start detection only after touch held for 5 sec ---
def on_held():
    global program_started
    if not program_started:
        print("Touch held for 5 seconds. Starting system...")
        program_started = True
        run_detection()

# Bind the held event
touch_sensor.when_held = on_held

# Keep the script alive until touch is held
print("Touch and hold the sensor for 5 seconds to start.")
pause()
