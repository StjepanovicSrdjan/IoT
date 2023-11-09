import threading
import time
from settings import load_settings
from components.DPIR1 import run_dpir
from components.RPIR import run_rpir
from components.DL import run_dl
from components.UDS import run_uds
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
    motion_event = threading.Event()
    light_on_by_motion_event = threading.Event()
    
    keyboard_callback = lambda key: on_key_event(key, lighton_event)
    keyboard.hook(keyboard_callback)
    try:
        run_dpir(settings['DPIR1'], threads, light_on_by_motion_event, motion_event, stop_event)
        run_rpir(settings['RPIR1'], threads, stop_event)
        run_rpir(settings['RPIR2'], threads, stop_event)
        run_dl(settings['DL'], threads, light_on_by_motion_event, lighton_event, stop_event)
        # run_uds(settings['DUS1'], threads, motion_event, stop_event)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('STOPPING...')
        for t in threads:
            stop_event.set()


