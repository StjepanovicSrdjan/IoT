import time
import random

def simulate_motions():
    while True:
        yield random.random()


def run_rpir_simulator(callback, name, stop_event):
    for m in simulate_motions():
        time.sleep(1)
        if m > 0.9:
            callback(name)
            time.sleep(1)
        if stop_event.is_set():
            break