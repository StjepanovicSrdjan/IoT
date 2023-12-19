import RPi.GPIO as GPIO
import time


class DMS:
    def __init__(self, pin_R1, pin_R2, pin_R3, pin_R4, pin_C1, pin_C2, pin_C3, pin_C4):
        self.pin_R1 = pin_R1
        self.pin_R2 = pin_R2
        self.pin_R3 = pin_R3
        self.pin_R4 = pin_R4
        self.pin_C1 = pin_C1
        self.pin_C2 = pin_C2
        self.pin_C3 = pin_C3
        self.pin_C4 = pin_C4

    def start_reading(self, callback, stop_event, publish_event, settings):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin_R1, GPIO.OUT)
        GPIO.setup(self.pin_R2, GPIO.OUT)
        GPIO.setup(self.pin_R3, GPIO.OUT)
        GPIO.setup(self.pin_R4, GPIO.OUT)

        GPIO.setup(self.pin_C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pin_C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pin_C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pin_C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        while True:
            self.read_line(self.pin_R1, ["1", "2", "3", "A"], callback, publish_event, settings)
            self.read_line(self.pin_R2, ["4", "5", "6", "B"], callback, publish_event, settings)
            self.read_line(self.pin_R3, ["7", "8", "9", "C"], callback, publish_event, settings)
            self.read_line(self.pin_R4, ["*", "0", "#", "D"], callback, publish_event, settings)
            time.sleep(0.2)

            if stop_event.is_set():
                break

    def read_line(self, line, characters, callback, publish_event, settings):
        GPIO.output(line, GPIO.HIGH)
        if GPIO.input(self.pin_C1) == 1:
            callback(characters[0], publish_event, settings)
        if GPIO.input(self.pin_C2) == 1:
            callback(characters[1], publish_event, settings)
        if GPIO.input(self.pin_C3) == 1:
            callback(characters[2], publish_event, settings)
        if GPIO.input(self.pin_C4) == 1:
            callback(characters[3], publish_event, settings)
        GPIO.output(line, GPIO.LOW)


def run_dms(dms, callback, stop_event, publish_event, settings):
    dms.start_reading(callback, stop_event, publish_event, settings)
