import threading
import time
from settings import load_settings
from components.DPIR1 import run_dpir
from components.DL import run_dl
import keyboard

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def on_key_event(key, light_event):
    if key.name == 'l' and key.event_type == keyboard.KEY_DOWN:
        light_event.set()




if __name__ == '__main__':
    print('STARTING...')
    
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    lighton_event = threading.Event()
    keyboard_callback = lambda key: on_key_event(key, lighton_event)
    keyboard.hook(keyboard_callback)
    try:
        dpir1_settings = settings['DPIR1']
        dl_settings = settings['DL']
        run_dpir(dpir1_settings, threads, stop_event)
        run_dl(dl_settings, threads, lighton_event, stop_event)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('STOPPING...')
        for t in threads:
            stop_event.set()


