import threading
import time

from simulators.DB_sim import run_db_simulator


def run_db(settings, threads, buzz_event, stop_event):
    if settings['simulated']:
        print('Starting DB simulation')
        dl_thread = threading.Thread(target=run_db_simulator, args=(buzz_event, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        print('DB simulator started')
    else:
        from actuators.DB_act import run_db_act, DB
        print('Starting DB actuator')
        dl = DB(settings['pin'], settings['pitch'], settings['duration'])
        dl_thread = threading.Thread(target=run_db_act, args=(dl, buzz_event, stop_event))
        threads.append(dl_thread)
        print('DB actuator started')
