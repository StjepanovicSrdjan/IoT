import time 


def run_dl_simulator(callback_on, callback_off, motion_event, light_event, stop_event):
    is_on = False
    while True:

        if light_event.is_set():
            light_event.clear()
            if is_on:
                is_on = False
                callback_off()
                continue
            if not is_on:
                is_on = True
                callback_on()
                continue

        if motion_event.is_set():
            motion_event.clear()
            callback_on()
            time.sleep(3)
            callback_off()
            is_on = False

        time.sleep(1)

        if stop_event.is_set():
            break
