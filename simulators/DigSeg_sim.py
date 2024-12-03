from datetime import datetime
import time

def run_digSeg_sim(stop_event, screen_event):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time 4Dig7Seg =", current_time)
        time.sleep(2)
        if screen_event.is_set():
            print('Screen colored in white')
            time.sleep(0.5)
            screen_event.clear()

        if stop_event.is_set():
            break