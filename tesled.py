import time
from gpiozero import LED

# Initialize LEDs
leds = [LED(27), LED(22), LED(23)]

current_led = 0
switch_time = 0.2  # Time each LED stays ON (in seconds)
last_switch = time.time()

while True:
    # Check if it's time to switch
    if time.time() - last_switch >= switch_time:
        # Turn off all LEDs
        for led in leds:
            led.off()

        # Turn on the next LED
        leds[current_led].on()

        # Move to the next LED
        current_led = (current_led + 1) % len(leds)  # Cycle through 0,1,2

        # Update last switch time
        last_switch = time.time()
