import RPi.GPIO as GPIO
import time

class UDS(object):

    def __init__(self, trig_pin, echo_pin) -> None:
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

    def set_pin(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(0.2)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(self.echo_pin) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.echo_pin) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300)/2
        return distance
    

def run_uds_sen(uds, callback, stop_event, publish_event, settings, entering_callback):
    uds.set_pin()
    last_dist = None
    count_exit = 0
    count_enter = 0
    while True:
        distance = uds.get_distance()
        if distance is not None:
            if last_dist is None:
                last_dist = distance
            else:
                if last_dist > distance:
                    count_enter += 1
                    if count_enter == 3:
                        count_enter = 0
                        count_exit = 0
                        entering_callback("Enter", settings)
                else:
                    count_exit += 1
                    if count_exit == 3:
                        count_enter = 0
                        count_exit = 0
                        entering_callback("Exit", settings)
            callback(distance, publish_event, settings)
        time.sleep(1)

        if stop_event.is_set():
            break
