import RPi.GPIO as GPIO
import time
from threading import Event
from collections import deque
from bt_speak import AlertMode
from utils import IntervalExponentialBackOff

notification_interval = 10
backoff_interval = IntervalExponentialBackOff()


def check_moisture(moisture_event: Event, alert_q: deque):
    # Set up GPIO pin
    sensor_pin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor_pin, GPIO.IN)

    try:
        while True:
            if GPIO.input(sensor_pin) == GPIO.HIGH:
                if not moisture_event.is_set() or backoff_interval.back_off_passed():
                    print("Water needed, queueing up alert")
                    moisture_event.set()
                    alert_q.append(AlertMode.NEED_WATER)
                    backoff_interval.set()
                else:
                    print("Water alert already queued")
            else:
                print("Checked soil. Is wet, no need watering.")
                if moisture_event.is_set():
                    moisture_event.clear()
                    backoff_interval.reset()

            time.sleep(notification_interval)
    except KeyboardInterrupt:
        # clean up resources used to avoid damage to RPi
        GPIO.cleanup()
