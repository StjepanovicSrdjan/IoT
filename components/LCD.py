import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from queue import Queue
from simulators.LCD_sim import run_lcd_sim


def run_lcd(settings, threads, stop_event, mess_queue, lcd_event):
    if settings['isOn']:
        from display.LCD.LCD1602 import run
        print('Starting LCD')
        dl_thread = threading.Thread(target=run, args=(stop_event, settings, mess_queue, lcd_event))
        dl_thread.start()
        threads.append(dl_thread)
        print('LCD started')
    else:
        print('Starting LCD simulation')
        dl_thread = threading.Thread(target=run_lcd_sim, args=(stop_event, mess_queue, lcd_event))
        dl_thread.start()
        threads.append(dl_thread)
        print('LCD simulation started')
