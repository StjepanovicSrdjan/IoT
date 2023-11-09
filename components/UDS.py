import threading
import time
from simulators.UDS_sim import run_uds_simulation

def uds_callback(dis):
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DISTANCE: " + str(dis))


def run_uds(settings, threads, motion_event, stop_event):
    if settings['simulated']:
        print('Starting DUS1 simulation')
        uds_thread = threading.Thread(target=run_uds_simulation, args=(uds_callback, motion_event, stop_event))
        uds_thread.start()
        threads.append(uds_thread)
        print('UDS simulator started')
    else:
        from sensors.UDS_sen import UDS, run_uds_sen
        print('Starting DUS1 sensor')
        uds = UDS(settings['trig_pin'], settings['echo_pin'])
        uds_thread = threading.Thread(target=run_uds_sen, args=(uds, uds_callback, stop_event))
        uds_thread.start()
        threads.append(uds_thread)
        print('DUS1 sensor started')