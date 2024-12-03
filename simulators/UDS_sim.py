import time 
import random

def simulate_closing_distance(callback, publish_event, settings, entering_callback):
    dist = 3.
    while dist > 0.:
        callback(dist, publish_event, settings)
        dist = random.uniform(dist - 1., dist)
        time.sleep(0.8)
    entering_callback("Enter", settings)

def simulate_growing_distance(callback, publish_event, settings, entering_callback):
    dist = 0.
    while dist < 3.:
        callback(dist, publish_event, settings)
        dist = random.uniform(dist, dist + 1.)
        time.sleep(0.8)
    entering_callback("Exit", settings)

def run_uds_simulation(callback, motion_event, stop_event, publish_event, settings, entering_callback):
    while True:
        time.sleep(1)
        if motion_event.is_set():
            motion_event.clear()
            if random.random() > 0.3:
                simulate_closing_distance(callback, publish_event, settings, entering_callback)
            else:
                simulate_growing_distance(callback, publish_event, settings, entering_callback)    
        if stop_event.is_set():
            break
