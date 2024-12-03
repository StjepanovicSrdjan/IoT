import time
import random


def simulate_motions():
    while True:
        yield random.random()


def run_dpir_simulator(callback,light_on_event, motion_event, stop_event, publish_event, settings):
    for m in simulate_motions():
        time.sleep(1)
        if m > 0.5:
            callback(light_on_event, publish_event, settings)
            motion_event.set()
            time.sleep(1)
        if stop_event.is_set():
            break
