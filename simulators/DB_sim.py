import time


def buzz():
    t = time.localtime()
    print('='*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("BUZZ!")


def run_db_simulator(buzz_event, stop_event):
    while True:
        if buzz_event.is_set():
            buzz_event.clear()
            buzz()

        time.sleep(1)

        if stop_event.is_set():
            break
