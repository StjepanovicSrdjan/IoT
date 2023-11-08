import threading
import time
from settings import load_settings

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == '__main__':
    print('STARTING...')
    settings = load_settings()
