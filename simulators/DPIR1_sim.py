import time
import random

def simulate_motions():
    while True:
        yield random.random()


def run_dpir_simulator(callback, stop_event):
    for m in simulate_motions():
        time.sleep(1.5)
        if m > 0.8:
            callback()
        if stop_event.is_set():
            break


