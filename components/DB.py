import threading
import time
from simulators.DB_sim import run_db_simulator
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

db_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, db_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_db_batch = db_batch.copy()
            publish_data_counter = 0
            db_batch.clear()
        publish.multiple(local_db_batch, hostname=HOSTNAME, port=PORT)
        print(f'\nPublished {publish_data_limit} DB values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, db_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def db_callback(publish_event, settings):
    global publish_data_counter, publish_data_limit
    payload = {
        "measurement": "DB",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": "BUZZ"
    }
    with counter_lock:
        db_batch.append(('DB', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_db(settings, threads, buzz_event, stop_event):
    global publish_data_limit
    publish_data_limit = settings['batch_size']
    if settings['simulated']:
        print('Starting DB simulation')
        dl_thread = threading.Thread(target=run_db_simulator, args=(db_callback, buzz_event, stop_event, publish_event, settings))
        dl_thread.start()
        threads.append(dl_thread)
        print('DB simulator started')
    else:
        from actuators.DB_act import run_db_act, DB
        print('Starting DB actuator')
        dl = DB(settings['pin'], settings['pitch'], settings['duration'])
        dl_thread = threading.Thread(target=run_db_act, args=(dl, db_callback, buzz_event, stop_event, publish_event, settings))
        threads.append(dl_thread)
        print('DB actuator started')
