import threading
import time
import random

from simulators.DS1_sim import run_ds_simulator


def door_open_callback():
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DOOR OPENED!")


def door_close_callback():
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DOOR CLOSED!")


def run_ds(settings, threads, open_event, stop_event):
    if settings['simulated']:
        print('Starting DS1 simulation')
        ds_thread = threading.Thread(
            target=run_ds_simulator,
            args=(door_open_callback, door_close_callback, open_event, stop_event)
        )
        ds_thread.start()

        threads.append(ds_thread)
        print('DS simulator started')
    else:
        from sensors.DS1_sen import DS, run_ds_sen
        print('Starting DS1 sensor')
        ds = DS(settings['pin'])
        ds_thread = threading.Thread(
            target=run_ds_sen,
            args=(ds, door_open_callback, door_close_callback, stop_event)
        )
        ds_thread.start()
        threads.append(ds_thread)
        print('DS1 sensor started')
