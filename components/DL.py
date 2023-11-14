import threading
import time
from simulators.DL_sim import run_dl_simulator

def dl_on_callback():
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print('The door light is ON!')

def dl_off_callback():
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print('The door light is OFF!')


def run_dl(settings, threads, motion_event, light_event, stop_event):
    if settings['simulated']:
        print('Starting DL simulation')
        dl_thread = threading.Thread(target=run_dl_simulator, args=(dl_on_callback, dl_off_callback, motion_event, light_event, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        print('DL simulator started')
    else:
        from actuators.DL_act import run_dl_act, DL
        print('Starting DL actuator')
        dl = DL(settings['pin'])
        dl_thread = threading.Thread(target=run_dl_act, args=(dl, light_event, stop_event))
        threads.append(dl_thread)
        print('DL actuator started')