import json
import threading
import time
from queue import Queue 
from components.DHT import run_dht
from components.DS1 import run_ds
# from components.LCD import run_lcd
from components.RPIR import run_rpir
from components.UDS import run_uds
from components.DPIR1 import run_dpir
from components.DB import run_db
from components.IR import run_ir
from components.RGB import run_rgb
from components.DigSegDisplay import run_dig
import paho.mqtt.client as mqtt

from settings import load_settings

import keyboard

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def on_key_event(key, open_event, buzz_event, ir_event, ir_queue):
    if key.name == 'd' and key.event_type == keyboard.KEY_DOWN:
        open_event.set()
    elif key.name == 'd' and key.event_type == keyboard.KEY_UP:
        open_event.clear()
    elif key.name == 'b' and key.event_type == keyboard.KEY_DOWN:
        buzz_event.set()
    elif key.name == '1' and key.event_type == keyboard.KEY_DOWN:
        ir_event.set()
        ir_queue.put(1)
    elif key.name == '2' and key.event_type == keyboard.KEY_DOWN:
        ir_event.set()
        ir_queue.put(2)
    elif key.name == '3' and key.event_type == keyboard.KEY_DOWN:
        ir_event.set()
        ir_queue.put(3)
    elif key.name == '4' and key.event_type == keyboard.KEY_DOWN:
        ir_event.set()
        ir_queue.put(4)
    elif key.name == '5' and key.event_type == keyboard.KEY_DOWN:
        ir_event.set()
        ir_queue.put(5)


if __name__ == '__main__':
    print('STARTING...')

    settings = load_settings()
    threads = []

    stop_event = threading.Event()
    open_event = threading.Event()
    motion_event = threading.Event()
    buzz_event = threading.Event()
    screen_event = threading.Event()
    ir_event = threading.Event()
    light_on_by_motion_event = threading.Event()

    ir_queue = Queue()

    def keyboard_callback(key):
        on_key_event(key, open_event, buzz_event, ir_event, ir_queue)
    keyboard.hook(keyboard_callback)

    try:
        run_rpir(settings['RPIR4'], threads, stop_event)
        run_dht(settings['RDHT4'], threads, stop_event, "RDHT4")
        run_db(settings['BB'], threads, buzz_event, stop_event)
        run_ir(settings['BIR'], threads, stop_event, ir_event, ir_queue)
        run_rgb(settings['BRGB'], threads, stop_event, ir_event, ir_queue)
        run_dig(settings['B4SD'], threads, stop_event, screen_event)

        # MQTT Configuration
        mqtt_client = mqtt.Client()
        mqtt_client.connect("localhost", 1883, 60)
        mqtt_client.loop_start()

        def on_connect(client, userdata, flags, rc):
            client.subscribe("WAKE_UP")
            print("Connected to MQTT broker")

        def wake_up_call():
            print("WAKE UP CALL")
            buzz_event.set()
            screen_event.set()

        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = lambda client, userdata, msg: wake_up_call()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('STOPPING...')
        for t in threads:
            stop_event.set()
