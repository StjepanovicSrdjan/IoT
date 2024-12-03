import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from simulators.RGB_sim import run_rgb_simulator

rgb_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, rgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_db_batch = rgb_batch.copy()
            publish_data_counter = 0
            rgb_batch.clear()
        publish.multiple(local_db_batch, hostname=HOSTNAME, port=PORT)
        print(f'\nPublished {publish_data_limit} RGB values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rgb_callback(publish_event, action, settings):
    global publish_data_counter, publish_data_limit
    payload = {
        "measurement": "RGB",
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": action
    }
    with counter_lock:
        rgb_batch.append(('RGB', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_rgb(settings, threads, stop_event, ir_event, mess_queue):
    global publish_data_limit
    publish_data_limit = settings['batch_size']
    if settings['simulated']:
        print('Starting RGB simulation')
        rgb_thread = threading.Thread(target=run_rgb_simulator, args=(rgb_callback, settings, stop_event, ir_event, mess_queue, publish_event))
        rgb_thread.start()
        threads.append(rgb_thread)
        print('RGB simulator started')
    else:
        from actuators.RGB_act import run_rgb_act
        print('Starting RGB actuator')
        rgb_thread = threading.Thread(target=run_rgb_act, args=(rgb_callback, settings, stop_event, ir_event, mess_queue, publish_event))
        rgb_thread.start()
        threads.append(rgb_thread)
        print('RGB actuator started')