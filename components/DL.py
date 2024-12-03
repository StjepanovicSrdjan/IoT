import threading
import time
from simulators.DL_sim import run_dl_simulator
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

dl_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dl_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = dl_batch.copy()
            publish_data_counter = 0
            dl_batch.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'\nPublished {publish_data_limit} DL values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dl_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dl_callback(publish_event, dl_settings, action):
    global publish_data_counter, publish_data_limit
    payload = {
        "measurement": "DL",
        "simulated": dl_settings['simulated'],
        "runs_on": dl_settings["runs_on"],
        "name": dl_settings["name"],
        "value": action
    }
    with counter_lock:
        dl_batch.append(('DL', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print('The door light is ' + action + '!')
  


def dl_off_callback():
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print('The door light is OFF!')


def run_dl(settings, threads, motion_event, light_event, stop_event):
    global publish_data_limit
    publish_data_limit = settings['batch_size']
    if settings['simulated']:
        print('Starting DL simulation')
        dl_thread = threading.Thread(target=run_dl_simulator, args=(dl_callback, motion_event, light_event, stop_event, publish_event, settings))
        dl_thread.start()
        threads.append(dl_thread)
        print('DL simulator started')
    else:
        from actuators.DL_act import run_dl_act, DL
        print('Starting DL actuator')
        dl = DL(settings['pin'])
        dl_thread = threading.Thread(target=run_dl_act, args=(dl, dl_callback, light_event, stop_event, publish_event, settings))
        dl_thread.start()
        threads.append(dl_thread)
        print('DL actuator started')
