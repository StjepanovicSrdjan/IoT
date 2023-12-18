import time 
import random

def simulate_closing_distance(callback, publish_event, settings):
    dist = 3.
    while dist > 0.:
        callback(dist, publish_event, settings)
        dist = random.uniform(dist - 1., dist)
        time.sleep(0.8)

def run_uds_simulation(callback, motion_event, stop_event, publish_event, settings):
    while True:
        time.sleep(1)
        if motion_event.is_set():
            motion_event.clear()
            simulate_closing_distance(callback, publish_event, settings)
        
        if stop_event.is_set():
            break
