import threading
import time
from queue import Queue 
from components.DHT import run_dht
from components.DS1 import run_ds
# from components.LCD import run_lcd
from components.RPIR import run_rpir
from components.UDS import run_uds
from components.DPIR1 import run_dpir
from components.Gyroscope import run_gyro


from settings import load_settings

import keyboard

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def on_key_event(key, open_event):
    if key.name == 'd' and key.event_type == keyboard.KEY_DOWN:
        open_event.set()
    elif key.name == 'd' and key.event_type == keyboard.KEY_UP:
        open_event.clear()



if __name__ == '__main__':
    print('STARTING...')

    settings = load_settings()
    threads = []

    stop_event = threading.Event()
    open_event = threading.Event()
    motion_event = threading.Event()
    light_on_by_motion_event = threading.Event()


    def keyboard_callback(key):
        on_key_event(key, open_event)
    keyboard.hook(keyboard_callback)
    lcd_queue = Queue()
    try:
        run_dht(settings['GDHT'], threads, stop_event, "GDHT", lcd_queue)
        run_ds(settings['DS2'], threads, open_event, stop_event)
        # run_ds(settings['GLCD'], threads, stop_event, lcd_queue)
        run_rpir(settings['RPIR3'], threads, stop_event)
        run_dpir(settings['DPIR2'], threads, light_on_by_motion_event, motion_event, stop_event)
        run_dht(settings['DHT3'], threads, stop_event, "DHT3")
        run_uds(settings['DUS2'], threads, motion_event, stop_event)
        run_gyro(settings['GSG'], threads, stop_event)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('STOPPING...')
        for t in threads:
            stop_event.set()
