import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from queue import Queue
from simulators.DigSeg_sim import run_digSeg_sim


def run_dig(settings, threads, stop_event, screen_event):
    if settings['isOn']:
        from display.DigSeg import run_4dig_dis
        print('Starting 4 Digit 7 Seg display')
        dig_thread = threading.Thread(target=run_4dig_dis, args=(settings, stop_event, screen_event))
        dig_thread.start()
        threads.append(dig_thread)
        print('4 Digit 7 Seg display started')
    else:
        print('Starting 4 Digit 7 Seg display simulation')
        dig_thread = threading.Thread(target=run_digSeg_sim, args=(stop_event, screen_event))
        dig_thread.start()
        threads.append(dig_thread)
        print('4 Digit 7 Seg display simulation started')