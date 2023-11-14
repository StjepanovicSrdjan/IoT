from simulators.DHT_sim import run_dht_simulator
import threading
import time


def dht_callback(name):
    def callback(humidity, temperature):
        t = time.localtime()
        print("=" * 20)
        print(f"{name} data:")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")
    return callback


def run_dht(settings, threads, stop_event, name):
    if settings['simulated']:
        print(f"Starting {name} simulator")
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback(name), stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f"{name} simulator started")
    else:
        from sensors.DHT_sen import run_dht_loop, DHT
        print(f"Starting {name} loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback(name), stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f"{name} loop started")
