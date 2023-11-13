import time


def run_ds_simulator(callback_open, callback_close, open_event, stop_event):
    while True:
        time.sleep(1)
        if open_event.is_set():
            callback_open()
            time.sleep(2)
            callback_close()

        if stop_event.is_set():
            break
