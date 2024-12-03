import RPi.GPIO as GPIO
import time

class DS:
    def __init__(self, pin):
        self.pin = pin
        self.start_time = None

    def start_detection(self, callback, publish_event, settings):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            self.pin, GPIO.BOTH,
            callback=self.button_pressed(callback, publish_event, settings),
            bouncetime=100
        )

    def get_state(self):
        return GPIO.input(self.pin) == GPIO.LOW

    def button_pressed(self, callback, publish_event, settings):
        def _callback(*args, **kwargs):
            if self.get_state():
                self.start_time = time.time()
                # callback(publish_event, settings, "Door opened.")
            else:
                if self.start_time is not None:
                    duration = time.time() - self.start_time
                    self.start_time = None
                    callback(publish_event, settings, duration)

        return _callback

    def __del__(self):
        GPIO.cleanup()


def run_ds_sen(ds, callback, stop_event, publish_event, settings):
    ds.start_detection(callback, publish_event, settings)
    while True:
        if stop_event.is_set():
            break
