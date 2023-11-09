import RPi.GPIO as GPIO
import time

class DPIR(object):

    def __init__(self, pin):
        self.pin = pin

    def detect_motion(self, func):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=func)




def run_dpir_sen(dpir, callback, stop_event):
    dpir.detect_motion(callback)
    while True:
        if stop_event.is_set():
            break
