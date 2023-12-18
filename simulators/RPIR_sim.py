import time
import random

def simulate_motions():
    while True:
        yield random.random()


def run_rpir_simulator(callback, stop_event, publish_event, settings):
    for m in simulate_motions():
        time.sleep(1)
        if m > 0.5:
            callback(publish_event, settings)
            time.sleep(1)
        if stop_event.is_set():
            break