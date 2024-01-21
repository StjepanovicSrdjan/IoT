import time
import random


def run_ds_simulator(callback, open_event, stop_event, publish_event, settings):
    while True:
        time.sleep(1)
        if random.random() > 0.7:
            duration = random.uniform(1.0 , 7.0 )
            callback(publish_event, settings, "Button pressed for:" + str(duration))
            # time.sleep(2)
            # callback(publish_event, settings, "Door closed.")

        if stop_event.is_set():
            break
