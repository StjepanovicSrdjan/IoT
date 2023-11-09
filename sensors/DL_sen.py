import RPi.GPIO as GPIO
import time

class DL(object):

    def __init__(self, pin) -> None:
        self.pin = pin
        self.is_on = False

    def set_pin(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def switch(self):
        if self.is_on:
            GPIO.output(self.pin,GPIO.LOW)
        else:
            GPIO.output(self.pin,GPIO.HIGH)

        self.is_on = not self.is_on

    def on_by_motion(self):
        GPIO.output(self.pin,GPIO.HIGH)
        time.sleep(3)
        GPIO.output(self.pin,GPIO.LOW)

        self.is_on = False


def run_dl_sen(dl, motion_event, light_event, stop_event):
    dl.set_pin()
    while True:
        time.sleep(1)
        if light_event.is_set():
            light_event.clear()
            dl.switch()
        
        if motion_event.is_set():
            motion_event.clear()
            dl.on_by_motion()
            
        if stop_event.is_set():
            break