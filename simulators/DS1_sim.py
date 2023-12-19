import time


def run_ds_simulator(callback, open_event, stop_event, publish_event, settings):
    while True:
        time.sleep(1)
        if open_event.is_set():
            callback(publish_event, settings, "Door opened.")
            time.sleep(2)
            callback(publish_event, settings, "Door closed.")

        if stop_event.is_set():
            break
