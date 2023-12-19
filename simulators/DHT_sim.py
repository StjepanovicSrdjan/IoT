import time
import random


def generate_values(initial_temp=25, initial_humidity=20):
    temperature = initial_temp
    humidity = initial_humidity
    while True:
        temperature = temperature + random.randint(-1, 1)
        humidity = humidity + random.randint(-1, 1)
        if humidity < 0:
            humidity = 0
        if humidity > 100:
            humidity = 100
        yield humidity, temperature


def run_dht_simulator(delay, callback, stop_event, publish_event, settings):
    for h, t in generate_values():
        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(h, t, publish_event, settings)
        if stop_event.is_set():
            break
