from simulators.DHT_sim import run_dht_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dth_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dth_batch, hostname=HOSTNAME, port=PORT)
        print(f'\nPublished {publish_data_limit} DHT values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dht_callback(humidity, temperature, publish_event, dht_settings, mess_queue):
    if mess_queue:
        mess_queue.put([temperature, humidity])
    global publish_data_counter, publish_data_limit
    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": humidity
    }

    with counter_lock:
        dht_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event, name, mess_queue=None):
    global publish_data_limit
    publish_data_limit = settings['batch_size']
    if settings['simulated']:
        print(f"Starting {name} simulator")
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, publish_event, settings, mess_queue))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f"{name} simulator started")
    else:
        from sensors.DHT_sen import run_dht_loop, DHT
        print(f"Starting {name} loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, publish_event, settings, mess_queue))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f"{name} loop started")
