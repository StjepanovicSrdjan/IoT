import RPi.GPIO as GPIO
import time

class DL(object):

    def __init__(self, pin) -> None:
        self.pin = pin
        self.is_on = False

    def set_pin(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def switch(self, callback, publish_event, settings):
        if self.is_on:
            GPIO.output(self.pin,GPIO.LOW)
            callback(publish_event, settings, "OFF")
        else:
            GPIO.output(self.pin,GPIO.HIGH)
            callback(publish_event, settings, "ON")


        self.is_on = not self.is_on

    def on_by_motion(self, callback, publish_event, settings):
        GPIO.output(self.pin,GPIO.HIGH)
        callback(publish_event, settings, "ON")
        time.sleep(3)
        GPIO.output(self.pin,GPIO.LOW)
        callback(publish_event, settings, "OFF")

        self.is_on = False


def run_dl_act(dl,callback, motion_event, light_event, stop_event, publish_event, settings):
    dl.set_pin()
    while True:
        time.sleep(1)
        if light_event.is_set():
            light_event.clear()
            dl.switch(callback, publish_event, settings)
        
        if motion_event.is_set():
            motion_event.clear()
            dl.on_by_motion(callback, publish_event, settings)
            
        if stop_event.is_set():
            break