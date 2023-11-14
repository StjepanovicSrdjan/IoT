import threading
import time

from components.DB import run_db
from components.DMS import run_dms
from components.DS1 import run_ds
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


def on_key_event(key, light_event, open_event, buzz_event):
    if key.name == 'l' and key.event_type == keyboard.KEY_DOWN:
        light_event.set()
    elif key.name == 'l' and key.event_type == keyboard.KEY_UP:
        light_event.clear()
    elif key.name == 'd' and key.event_type == keyboard.KEY_DOWN:
        open_event.set()
    elif key.name == 'd' and key.event_type == keyboard.KEY_UP:
        open_event.clear()
    elif key.name == 'b' and key.event_type == keyboard.KEY_DOWN:
        buzz_event.set()


if __name__ == '__main__':
    print('STARTING...')

    settings = load_settings()
    threads = []

    stop_event = threading.Event()
    lighton_event = threading.Event()
    motion_event = threading.Event()
    open_event = threading.Event()
    buzz_event = threading.Event()
    light_on_by_motion_event = threading.Event()

    def keyboard_callback(key):
        on_key_event(key, lighton_event, open_event, buzz_event)
    keyboard.hook(keyboard_callback)

    try:
        run_dpir(settings['DPIR1'], threads, light_on_by_motion_event, motion_event, stop_event)
        run_rpir(settings['RPIR1'], threads, stop_event)
        run_rpir(settings['RPIR2'], threads, stop_event)
        run_dl(settings['DL'], threads, light_on_by_motion_event, lighton_event, stop_event)
        # run_uds(settings['DUS1'], threads, motion_event, stop_event)
        run_ds(settings['DS1'], threads, open_event, stop_event)
        run_db(settings['DB'], threads, buzz_event, stop_event)
        run_dms(settings['DB'], threads, stop_event)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('STOPPING...')
        for t in threads:
            stop_event.set()
