import threading
import time
import random

from simulators.DMS_sim import run_dms_simulator


def char_input_callback(c):
    t = time.localtime()
    print('=' * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Keyboard input $>> {c}")


def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print('Starting DMS simulation')
        ds_thread = threading.Thread(
            target=run_dms_simulator,
            args=(char_input_callback, stop_event)
        )
        ds_thread.start()

        threads.append(ds_thread)
        print('DS simulator started')
    else:
        from sensors.DMS_sen import DMS, run_dms
        print('Starting DMS sensor')
        ds = DMS(
            settings["R1"],
            settings["R2"],
            settings["R3"],
            settings["R4"],
            settings["C1"],
            settings["C2"],
            settings["C3"],
            settings["C4"],
        )
        ds_thread = threading.Thread(
            target=run_dms,
            args=(ds, char_input_callback, stop_event)
        )
        ds_thread.start()
        threads.append(ds_thread)
        print('DS1 sensor started')
