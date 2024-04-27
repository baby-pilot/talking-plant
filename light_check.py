import RPi.GPIO as GPIO
import time
from enum import Enum
from threading import Event
from collections import deque
from bt_speak import AlertMode
class MODE(Enum):
    HIGH = 1
    LOW = 0


GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

notification_interval = 10  # Interval in seconds between notifications

def check_light(light_event: Event, alert_q: deque):
    try:
        while True:
            sensor_output = GPIO.input(6)
            # print(f"sensor output: {sensor_output}")
            if sensor_output == MODE.HIGH.value:
                if not light_event.is_set():
                    print("More UV rays needed. Queueing up alert")
                    light_event.set()
                    alert_q.append(AlertMode.NEED_UV)
                else:
                    print("More UV rays needed, and is already queued.")
            else:
                print("Enuf sun, no move pls")
                if light_event.is_set():
                    light_event.clear()
                
            time.sleep(notification_interval)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program stopped by user.")
