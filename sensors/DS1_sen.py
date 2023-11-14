import RPi.GPIO as GPIO


class DS:
    def __init__(self, pin):
        self.pin = pin

    def start_detection(self, callback_open, callback_close):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            self.pin, GPIO.BOTH,
            callback=self.button_pressed(callback_open, callback_close),
            bouncetime=100
        )

    def get_state(self):
        return GPIO.input(self.pin) == GPIO.LOW

    def button_pressed(self, callback_open, callback_close):
        def callback(*args, **kwargs):
            if self.get_state():
                callback_open()
            else:
                callback_close()

        return callback

    def __del__(self):
        GPIO.cleanup()


def run_ds_sen(ds, callback_open, callback_close, stop_event):
    ds.start_detection(callback_open, callback_close)
    while True:
        if stop_event.is_set():
            break
