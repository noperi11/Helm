from gpiozero import Buzzer
from mpu6050 import mpu6050

class HeadTilt:
    def __init__(self, threshold_deg=6):
        self.mpu = mpu6050(0x68)
        self.threshold = threshold_deg

    def get_pitch(self):
        data = self.mpu.get_accel_data()
        pitch = data['y']
        return pitch

    def is_tilted(self):
        return abs(self.get_pitch()) > self.threshold
