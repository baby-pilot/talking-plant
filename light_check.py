import RPi.GPIO as GPIO
import time
from enum import Enum
from threading import Event

class MODE(Enum):
    HIGH = 0
    LOW = 1


GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

notification_interval = 5  # Interval in seconds between notifications

def check_light(light_event: Event):
    try:
        while True:
            sensor_output = GPIO.input(6)
            print(f"sensor output: {sensor_output}")
            if sensor_output == MODE.HIGH.value:
                print("More UV rays needed. Queueing up alert if not already set...")
                if not light_event.is_set():
                    light_event.set()
            else:
                print("Enuf sun, no move pls")
                if light_event.is_set():
                    light_event.clear()
                
            time.sleep(notification_interval)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program stopped by user.")
