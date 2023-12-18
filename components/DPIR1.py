import threading
import time
from simulators.DPIR1_sim import run_dpir_simulator
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

dpir_batch = []
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
        print(f'\nPublished {publish_data_limit} DPIR1 values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dpir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dpir_callback(light_on_event, publish_event, settings):
    global publish_data_counter, publish_data_limit
    t = time.localtime()
    payload = {
        "measurement": "DPIR",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": "Motion detected"
        }
    with counter_lock:
        dpir_batch.append(('DPIR', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    light_on_event.set()
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DPIR1 detected motion!")


def run_dpir(settings, threads, light_on_event, motion_event, stop_event):
    if settings['simulated']:
        print('Starting DPIR1 simulation')
        dpir1_thread = threading.Thread(target = run_dpir_simulator, args=(dpir_callback, light_on_event, motion_event, stop_event, publish_event, settings))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sumilator started")
    else:
        from sensors.PIR_sen import run_dpir_sen, PIR
        print('Startin DPIR1 sensor')
        dpir = PIR(settings['pin'])
        dpir1_thread = threading.Thread(target = run_dpir_sen, args=(dpir, dpir_callback, light_on_event, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sensor started")