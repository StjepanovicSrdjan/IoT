import RPi.GPIO as GPIO
import time

class PIR(object):

    def __init__(self, pin):
        self.pin = pin

    def detect_motion(self, func):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=func)




def run_dpir_sen(dpir, callback, light_on_event, stop_event):
    detect_callback = lambda light_on_evet: callback(light_on_event)
    dpir.detect_motion(detect_callback)
    while True:
        if stop_event.is_set():
            break

def run_rpir_sen(dpir, callback, name, stop_event):
    detect_callback = lambda name: callback(name)
    dpir.detect_motion(detect_callback)
    while True:
        if stop_event.is_set():
            break
