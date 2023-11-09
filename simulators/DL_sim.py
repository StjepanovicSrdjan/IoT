import time 
import random

def simulate_action():
    while True:
        yield random.random()

def run_dl_simulator(callback_on, callback_off, light_event, stop_event):
    is_on = False
    while True:

        if light_event.is_set():
            light_event.clear()
            if is_on:
                is_on = False
                callback_off()
                continue
            if not is_on:
                is_on = True
                callback_on()
                continue
        time.sleep(1)

        if stop_event.is_set():
            break
