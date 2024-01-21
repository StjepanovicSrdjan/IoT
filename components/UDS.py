import threading
import time
from simulators.UDS_sim import run_uds_simulation
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

uds_batch = []
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
        print(f'\nPublished {publish_data_limit} UDS values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, uds_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def uds_callback(dis, publish_event, settings):
    global publish_data_counter, publish_data_limit
    payload = {
        "measurement": "UDS",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": dis
        }
    with counter_lock:
        uds_batch.append(('UDS', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    # t = time.localtime()
    # print('='*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print("DISTANCE: " + str(dis))

def entering_callback(action, settings):
    # payload = {
    #     "Entrance": "PI1",
    #     "simulated": settings['simulated'],
    #     "runs_on": settings["runs_on"],
    #     "name": settings["name"],
    #     "value": action
    #     }
    print(action)
    publish.single(topic="Door", payload=action, hostname=HOSTNAME, port=PORT)

def run_uds(settings, threads, motion_event, stop_event):
    if settings['simulated']:
        print('Starting DUS1 simulation')
        uds_thread = threading.Thread(target=run_uds_simulation, args=(uds_callback, motion_event, stop_event, publish_event, settings, entering_callback))
        uds_thread.start()
        threads.append(uds_thread)
        print('UDS simulator started')
    else:
        from sensors.UDS_sen import UDS, run_uds_sen
        print('Starting DUS1 sensor')
        uds = UDS(settings['trig_pin'], settings['echo_pin'])
        uds_thread = threading.Thread(target=run_uds_sen, args=(uds, uds_callback, stop_event, publish_event, settings, entering_callback))
        uds_thread.start()
        threads.append(uds_thread)
        print('DUS1 sensor started')