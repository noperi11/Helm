from gpiozero import LED, Buzzer
from time import time, sleep
import threading

class AlertDevice:
    def __init__(self, led_pin=26, buzzer_pin=16):
        self.led = LED(led_pin)
        self.buzzer = Buzzer(buzzer_pin)
        self._alert_thread = None
        self._stop_flag = False
        self._override_active = False
        self._alert_in_progress = False

    def _eyes_closed_alert(self):
        self._alert_in_progress = True

        # First beep the buzzer for 0.2 seconds
        if not self._override_active:
            self.buzzer.on()
            sleep(0.2)
            self.buzzer.off()

            # Then blink the LED 3 times, completing the sequence regardless of eye state
            for _ in range(8):
                if self._override_active:  # Only override should stop the blinking
                    break
                self.led.on()
                sleep(0.2)
                self.led.off()
                sleep(0.2)

        self._alert_in_progress = False

    def start_alert(self):
        # Don't start a new alert if one is already in progress
        if self._alert_in_progress:
            return

        self._stop_flag = False
        self._alert_thread = threading.Thread(target=self._eyes_closed_alert)
        self._alert_thread.daemon = True  # This ensures the thread doesn't block program exit
        self._alert_thread.start()

    def stop_alert(self):
        # This now only stops future alerts, doesn't interrupt current ones
        self._stop_flag = True

        # If override is active, make sure devices are off when not overridden
        if not self._override_active and not self._alert_in_progress:
            self.led.off()
            self.buzzer.off()

    def start_override(self):
        self._override_active = True
        self.buzzer.on()
        self.led.on()

    def stop_override(self):
        self._override_active = False
        self.buzzer.off()
        self.led.off()
