import time
import random

def simulate_motions():
    while True:
        yield random.random()


def run_dpir_simulator(callback, motion_event, stop_event):
    for m in simulate_motions():
        time.sleep(1)
        if m > 0.8:
            callback()
            motion_event.set()
            time.sleep(2)
        if stop_event.is_set():
            break


