import time
from random import random, randint


def run_dms_simulator(callback, stop_event, publish_event, settings):
    while True:
        time.sleep(1)
        if random() > 0.5:
            for i in range(4):
                callback(randint(0, 9), publish_event, settings)
                time.sleep(0.5)
            time.sleep(2)

        if stop_event.is_set():
            break
