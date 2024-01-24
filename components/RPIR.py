import threading
import time
from simulators.RPIR_sim import run_rpir_simulator
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

rpir_batch = []
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
        print(f'\nPublished {publish_data_limit} RPIR values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rpir_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def rpir_callback(publish_event, settings):
    global publish_data_counter, publish_data_limit
    payload = {
        "measurement": "PIR",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": "Motion detected"
        }
    with counter_lock:
        rpir_batch.append(('PIR', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    # t = time.localtime()
    # print('='*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(settings['name'] + " detected motion!")


def run_rpir(settings, threads, stop_event):
    global publish_data_limit
    publish_data_limit = settings['batch_size']
    if settings['simulated']:
        print('Starting ' + settings['name'] + ' simulation')
        dpir1_thread = threading.Thread(target = run_rpir_simulator, args=(rpir_callback, stop_event, publish_event, settings))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print(settings['name'] + " sumilator started")
    else:
        from sensors.PIR_sen import run_rpir_sen, PIR
        print('Starting ' + settings['name'] + ' simulation')
        dpir = PIR(settings['pin'])
        dpir1_thread = threading.Thread(target = run_rpir_sen, args=(dpir, rpir_callback, stop_event, publish_event, settings))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print(settings['name'] + " sumilator started")
