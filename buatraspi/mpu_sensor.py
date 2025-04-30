import math
import board
import busio
from adafruit_mpu6050 import MPU6050

class HeadTilt:
    def __init__(self, threshold_deg=30):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = MPU6050(i2c)
        self.threshold = threshold_deg

    def get_pitch(self):
        ax, ay, az = self.mpu.acceleration
        pitch = math.degrees(math.atan2(ax, math.sqrt(ay**2 + az**2)))
        return pitch

    def is_tilted(self):
        return abs(self.get_pitch()) > self.threshold

