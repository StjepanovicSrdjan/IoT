import threading
import time
from simulators.DPIR1_sim import run_dpir_simulator

def dpir_callback():
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DPIR1 detected motion!")


def run_dpir(settings, threads, stop_event):
    if settings['simulated']:
        print('Startin DPIR1 simulation')
        dht1_thread = threading.Thread(target = run_dpir_simulator, args=(dpir_callback, stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 sumilator started")
    else:
        pass