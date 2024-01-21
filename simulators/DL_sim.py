import time 


def run_dl_simulator(callback, motion_event, light_event, stop_event, publish_event, settings):
    is_on = False
    while True:

        if light_event.is_set():
            light_event.clear()
            if is_on:
                is_on = False
                callback(publish_event, settings, "OFF")
                continue
            if not is_on:
                is_on = True
                callback(publish_event, settings,"ON")
                continue

        if motion_event.is_set():
            motion_event.clear()
            callback(publish_event, settings,'ON')
            time.sleep(10)
            callback(publish_event, settings,'OFF')
            is_on = False

        time.sleep(1)

        if stop_event.is_set():
            break
