import threading
import time
import random
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from simulators.DMS_sim import run_dms_simulator

dms_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_batch, hostname=HOSTNAME, port=PORT)
        print(f'\nPublished {publish_data_limit} DMS values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dms_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def char_input_callback(c, publish_event, settings):
    global publish_data_counter, publish_data_limit
    t = time.localtime()
    payload = {
        "measurement": "DMS",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": c
    }
    with counter_lock:
        dms_batch.append(('DMS', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    # print('=' * 20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Keyboard input $>> {c}")


def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print('Starting DMS simulation')
        ds_thread = threading.Thread(
            target=run_dms_simulator,
            args=(char_input_callback, stop_event, publish_event, settings)
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
            args=(ds, char_input_callback, stop_event, publish_event, settings)
        )
        ds_thread.start()
        threads.append(ds_thread)
        print('DS1 sensor started')
