import math
import time
import random

class GyroscopeSimulator:
    def __init__(self, initial_angle=90, angular_velocity=1):
        self.angle = initial_angle
        self.angular_velocity = angular_velocity

    def get_gyroscope_reading(self):
        gyro_reading = math.sin(math.radians(self.angle))
        self.angle += random.uniform(-10.0, 10.0) 
        return gyro_reading
    

def run_gyro_sim(callback, settings, stop_event, gyro_sim, publish_event):
    while True:
        gyro_reading = gyro_sim.get_gyroscope_reading()
        # print(f"Gyroscope Reading: {gyro_reading:.2f}")
        callback(gyro_reading, publish_event, settings)
        time.sleep(1)
        if stop_event.is_set():
            break
