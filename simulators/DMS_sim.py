import time
from random import random, randint


def run_dms_simulator(callback, stop_event):
    while True:
        time.sleep(1)
        if random() > 0.9:
            for i in range(4):
                callback(randint(0, 9))
                time.sleep(0.5)
            time.sleep(2)

        if stop_event.is_set():
            break
