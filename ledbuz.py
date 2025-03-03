from gpiozero import LED, Buzzer
from time import monotonic

led = LED(6)
buzzer = Buzzer(26)

blink_interval = 0.1  # seconds
blink_count = 8

last_toggle = monotonic()
state = False
counter = 0

while counter < blink_count * 2:  # Each cycle has ON and OFF
    now = monotonic()
    if now - last_toggle >= blink_interval:
        state = not state  # Toggle state
        led.value = state
        buzzer.value = state
        last_toggle = now
        counter += 1

led.off()
buzzer.off()
