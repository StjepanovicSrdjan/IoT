import threading
import time
from simulators.RPIR_sim import run_rpir_simulator

def rpir_callback(name):
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(name + " detected motion!")


def run_rpir(settings, threads, stop_event):
    if settings['simulated']:
        print('Starting ' + settings['name'] + ' simulation')
        dpir1_thread = threading.Thread(target = run_rpir_simulator, args=(rpir_callback, settings['name'], stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print(settings['name'] + " sumilator started")
    else:
        from sensors.PIR_sen import run_rpir_sen, PIR
        print('Starting ' + settings['name'] + ' simulation')
        dpir = PIR(settings['pin'])
        dpir1_thread = threading.Thread(target = run_rpir_sen, args=(dpir, rpir_callback, settings['name'], stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print(settings['name'] + " sumilator started")
