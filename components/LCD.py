import threading
import time
from display.LCD.LCD1602 import run
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from queue import Queue


def run_lcd(settings, threads, stop_event, mess_queue):
    if settings['isOn']:
        print('Starting LCD')
        dl_thread = threading.Thread(target=run, args=(stop_event, settings, mess_queue))
        dl_thread.start()
        threads.append(dl_thread)
        print('LCD started')
