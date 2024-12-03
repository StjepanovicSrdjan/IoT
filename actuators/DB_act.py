import RPi.GPIO as GPIO
import time


class DB:
    def __init__(self, pin, pitch, duration):
        self.duration = duration
        self.pitch = pitch
        self.pin = pin

    def activate(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def buzz(self):
        period = 1.0 / self.pitch
        delay = period / 2
        cycles = int(self.duration * self.pitch)
        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)

    def __del__(self):
        GPIO.cleanup()


def run_db_act(db, callback, buzz_event, stop_event, publish_event, settings):
    db.activate()
    while True:
        if buzz_event.is_set():
            db.buzz()
            callback(publish_event, settings)
            buzz_event.clear()
        if stop_event.is_set():
            break
        time.sleep(1)
