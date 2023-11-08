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
        dpir1_thread = threading.Thread(target = run_dpir_simulator, args=(dpir_callback, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sumilator started")
    else:
        from sensors.DPIR1_sen import run_dpir, DPIR
        print('Startin DPIR sensor')
        dpir = DPIR(settings['pin'])
        dpir1_thread = threading.Thread(target = run_dpir, args=(dpir, dpir_callback, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sensor started")