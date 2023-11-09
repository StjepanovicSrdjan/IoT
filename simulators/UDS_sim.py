import time 
import random

def simulate_closing_distance(callback):
    dist = 3.
    while dist > 0.:
        callback(dist)
        dist = random.uniform(dist - 0.7, dist)
        time.sleep(0.8)

def run_uds_simulation(callback, motion_event, stop_event):
    while True:
        time.sleep(1)
        if motion_event.is_set():
            motion_event.clear()
            simulate_closing_distance(callback)
        
        if stop_event.is_set():
            break
