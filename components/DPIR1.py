import threading
import time
from simulators.DPIR1_sim import run_dpir_simulator

def dpir_callback(light_on_event):
    light_on_event.set()
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DPIR1 detected motion!")


def run_dpir(settings, threads, light_on_event, motion_event, stop_event):
    if settings['simulated']:
        print('Starting DPIR1 simulation')
        dpir1_thread = threading.Thread(target = run_dpir_simulator, args=(dpir_callback, light_on_event, motion_event, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sumilator started")
    else:
        from sensors.PIR_sen import run_dpir_sen, PIR
        print('Startin DPIR1 sensor')
        dpir = PIR(settings['pin'])
        dpir1_thread = threading.Thread(target = run_dpir_sen, args=(dpir, dpir_callback, light_on_event, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sensor started")