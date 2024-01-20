import threading
import time
import random
from simulators.DS1_sim import run_ds_simulator
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

ds_batch = []
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
        print(f'\nPublished {publish_data_limit} DS values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_batch,))
publisher_thread.daemon = True
publisher_thread.start()



def door_callback(publish_event, settings, action):
    global publish_data_counter, publish_data_limit
    payload = {
        "measurement": "DS",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": action
        }
    with counter_lock:
        ds_batch.append(('DS', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DOOR " + action + "!")



def run_ds(settings, threads, open_event, stop_event):
    if settings['simulated']:
        print('Starting DS1 simulation')
        ds_thread = threading.Thread(
            target=run_ds_simulator,
            args=(door_callback, open_event, stop_event, publish_event, settings)
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
            args=(ds, door_callback, stop_event, publish_event, settings)
        )
        ds_thread.start()
        threads.append(ds_thread)
        print('DS1 sensor started')
