import RPi.GPIO as GPIO
from time import sleep

#disable warnings (optional)
# GPIO.setwarnings(False)

# GPIO.setmode(GPIO.BCM)

RED_PIN = 12
GREEN_PIN = 13
BLUE_PIN = 19
actions = ['RGB ON', 'RGB OFF', 'RGB RED', 'RGB BLUE', 'RGB GREEN']

# #set pins as outputs
# GPIO.setup(RED_PIN, GPIO.OUT)
# GPIO.setup(GREEN_PIN, GPIO.OUT)
# GPIO.setup(BLUE_PIN, GPIO.OUT)

def turnOff():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def white():
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def red():
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def green():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def blue():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def yellow():
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def purple():
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def lightBlue():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)

def run_rgb_act(callback, settings, stop_event, IRcommand_event, mess_queue, publish_event):
    RED_PIN = settings['red_pin']
    BLUE_PIN = settings['blue_pin']
    GREEN_PIN = settings['green_pin']

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    while True:
        if IRcommand_event.is_set():
            data = mess_queue.get()
            try:
                data = int(data)
                if data == 1:
                    white()
                    callback(publish_event, actions[data-1], settings)
                elif data == 2:
                    turnOff()
                    callback(publish_event, actions[data-1], settings)
                elif data == 3:
                    red()
                    callback(publish_event, actions[data-1], settings)
                elif data == 4:
                    blue()
                    callback(publish_event, actions[data-1], settings)
                elif data == 5:
                    green()
                    callback(publish_event, actions[data-1], settings)
            except:
                pass
            IRcommand_event.clear()
        if stop_event.is_set():
            break
