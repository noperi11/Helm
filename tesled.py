from gpiozero import LED
from time import sleep

a = LED(27)
b = LED(22)
c = LED(23)

while True:
    a.on()
    sleep(0.2)
    a.off()
    sleep(0.2)
    b.on()
    sleep(0.2)
    b.off()
    sleep(0.2)
    c.on()
    sleep(0.2)
    c.off()
    sleep(0.2)
