import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from simulators.IR_sim import run_ir_simulator

ir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, ir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_db_batch = ir_batch.copy()
            publish_data_counter = 0
            ir_batch.clear()
        publish.multiple(local_db_batch, hostname=HOSTNAME, port=PORT)
        print(f'\nPublished {publish_data_limit} IR values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def ir_callback(publish_event, action, settings):
    global publish_data_counter, publish_data_limit
    payload = {
        "measurement": "IR",
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": action
    }
    with counter_lock:
        ir_batch.append(('IR', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_ir(settings, threads, stop_event, ir_event, mess_queue):
    global publish_data_limit
    publish_data_limit = settings['batch_size']
    if settings['simulated']:
        print('Starting IR simulation')
        ir_thread = threading.Thread(target=run_ir_simulator, args=(ir_callback, settings, stop_event, ir_event, mess_queue, publish_event))
        ir_thread.start()
        threads.append(ir_thread)
        print('IR simulator started')
    else:
        from actuators.IR_act import run_ir_act
        print('Starting IR actuator')
        ir_thread = threading.Thread(target=run_ir_act, args=(ir_callback, settings, stop_event, publish_event, ir_event, mess_queue))
        ir_thread.start()
        threads.append(ir_thread)
        print('IR actuator started')