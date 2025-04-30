import cv2
import time
from threading import Thread
from gpiozero import LED, Buzzer

from eye_detection import EyeDetector
from mpu_sensor import HeadTilt

# Inisialisasi GPIO
led = LED(17)
buzzer = Buzzer(27)

# Inisialisasi detektor dan sensor
eye = EyeDetector()
head = HeadTilt(threshold_deg=30)

cap = cv2.VideoCapture(0)

def eye_alert():
    led.blink(on_time=0.5, off_time=0.5, n=8)
    buzzer.beep(on_time=0.5, off_time=0.5, n=8)
    buzzer.off()

eye_closed_start = None
eye_alerted = False

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        is_open, p, rect = eye.detect(frame)

        # Override oleh MPU6050
        if head.is_tilted():
            buzzer.on()
        else:
            buzzer.off()
            # Logika deteksi mata
            if not is_open:
                if eye_closed_start is None:
                    eye_closed_start = time.time()
                elif not eye_alerted and time.time() - eye_closed_start >= 1.2:
                    eye_alerted = True
                    Thread(target=eye_alert).start()
            else:
                eye_closed_start = None
                eye_alerted = False

        # Tampilkan hasil (opsional)
        color = (0,255,0) if is_open else (0,0,255)
        x1,y1,x2,y2 = rect
        cv2.rectangle(frame, (x1,y1),(x2,y2), color, 2)
        cv2.imshow('Smart Helm', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()

