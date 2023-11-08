import threading
import time
from settings import load_settings
from components.DPIR1 import run_dpir

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == '__main__':
    print('STARTING...')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        dpir1_settings = settings['DPIR1']
        run_dpir(dpir1_settings, threads, stop_event)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('STOPPING...')
        for t in threads:
            stop_event.set()


