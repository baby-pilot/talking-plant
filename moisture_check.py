import RPi.GPIO as GPIO
import time
from threading import Event
from collections import deque
from bt_speak import AlertMode

def check_moisture(moisture_event: Event, alert_q: deque):
    # Set up GPIO pin
    sensor_pin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor_pin, GPIO.IN)

    try:
        while True:
            if GPIO.input(sensor_pin) == GPIO.HIGH:
                if not moisture_event.is_set():
                    print("Water needed, queueing up alert")
                    moisture_event.set()
                    alert_q.append(AlertMode.NEED_WATER)
            else:
                print("Checked soil. Is wet, no need watering.")
                if moisture_event.is_set():
                    moisture_event.clear()
            time.sleep(2)
    except KeyboardInterrupt:
        # clean up resources used to avoid damage to RPi
        GPIO.cleanup()