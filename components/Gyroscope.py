from simulators.Gyro_sim import GyroscopeSimulator, run_gyro_sim
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

gyro_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, gyro_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dth_batch = gyro_batch.copy()
            publish_data_counter = 0
            gyro_batch.clear()
        publish.multiple(local_dth_batch, hostname=HOSTNAME, port=PORT)
        print(f'\nPublished {publish_data_limit} Gyroscope values.\n')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def gyro_callback( value, publish_event, settings):
    global publish_data_counter, publish_data_limit
    gyro_payload = {
        "measurement": "Gyroscope",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": value
    }


    with counter_lock:
        gyro_batch.append(('Gyroscope', json.dumps(gyro_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_gyro(settings, threads, stop_event):
    global publish_data_limit
    publish_data_limit = settings['batch_size']
    if settings['simulated']:
        print('Starting Gyroscope simulation')
        gyroSim = GyroscopeSimulator()
        gyro_thread = threading.Thread(
            target=run_gyro_sim,
            args=(gyro_callback, settings, stop_event, gyroSim, publish_event)
        )
        gyro_thread.start()

        threads.append(gyro_thread)
        print('Gyroscope simulator started')