import time
from gpiozero import Buzzer
from mpu6050 import mpu6050

# Create MPU6050 object
mpu = mpu6050(0x68)

# Create Buzzer object
buzzer = Buzzer(26)  # Change the GPIO pin as needed

# Function to read accelerometer data
def read_sensor_data():
    return mpu.get_accel_data()

while True:
    data = read_sensor_data()
    z_accel = data['y']
    print(z_accel)

    if abs(z_accel) >= 6:
        buzzer.on()  # Turn buzzer on
    else:
        buzzer.off()  # Turn buzzer off

    time.sleep(0.1)  # Small delay to prevent excessive looping
