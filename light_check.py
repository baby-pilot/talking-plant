import RPi.GPIO as GPIO
import time
from enum import Enum
from threading import Event
from collections import deque
from bt_speak import AlertMode
from utils import IntervalExponentialBackOff


class MODE(Enum):
    HIGH = 1
    LOW = 0


GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

notification_interval = 10  # Interval in seconds between notifications
backoff_interval = IntervalExponentialBackOff()


def check_light(light_event: Event, alert_q: deque):
    try:
        while True:
            sensor_output = GPIO.input(6)
            # print(f"sensor output: {sensor_output}")
            if sensor_output == MODE.HIGH.value:
                if not light_event.is_set() or backoff_interval.back_off_passed():
                    print("More UV rays needed. Queueing up alert")
                    light_event.set()
                    alert_q.append(AlertMode.NEED_UV)
                    backoff_interval.set()
                else:
                    print("UV alert already queued.")
            else:
                print("Enuf sun, no move pls")
                if light_event.is_set():
                    light_event.clear()
                    backoff_interval.reset()

            time.sleep(notification_interval)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program stopped by user.")
