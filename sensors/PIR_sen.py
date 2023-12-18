import RPi.GPIO as GPIO
import time

class PIR(object):

    def __init__(self, pin):
        self.pin = pin

    def detect_motion(self, func):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=func)




def run_dpir_sen(dpir, callback, light_on_event, stop_event, publish_event, settings):
    detect_callback = lambda _: callback(light_on_event, publish_event, settings)
    dpir.detect_motion(detect_callback)
    while True:
        if stop_event.is_set():
            break

def run_rpir_sen(dpir, callback, stop_event, publish_event, settings):
    detect_callback = lambda _: callback(publish_event, settings)
    dpir.detect_motion(detect_callback)
    while True:
        if stop_event.is_set():
            break
