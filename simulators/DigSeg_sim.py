from datetime import datetime
import time

def run_digSeg_sim(stop_event):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time 4Dig7Seg =", current_time)
        time.sleep(2)
        if stop_event.is_set():
            break