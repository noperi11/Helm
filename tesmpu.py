import mpu6050
import time
from gpiozero import Buzzer

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)
buzzer = Buzzer(27)  # Sesuaikan dengan pin GPIO yang digunakan

# Define a function to read the sensor data
def read_sensor_data():
    gyroscope_data = mpu6050.get_gyro_data()
    return gyroscope_data

head_down_start_time = None
THRESHOLD = 30  # Sesuaikan nilai threshold sesuai kebutuhan
DURATION = 2.0  # Waktu dalam detik

while True:
    gyroscope_data = read_sensor_data()
    gyro_z = gyroscope_data['z']

    if abs(gyro_z) > THRESHOLD:
        if head_down_start_time is None:
            head_down_start_time = time.time()
        elif time.time() - head_down_start_time >= DURATION:
            buzzer.on()
    else:
        head_down_start_time = None
        buzzer.off()

    print("Gyroscope data:", gyroscope_data)
    time.sleep(1)
