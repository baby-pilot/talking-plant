import RPi.GPIO as GPIO
import time
from send_sms import send_txt
from enum import Enum

class MODE(Enum):
    HIGH = 0
    LOW = 1


GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

notification_interval = 5  # Interval in seconds between notifications
last_notification_time = 0  # Time at which the last notification was sent

try:
    while True:
        current_time = time.time()
        sensor_output = GPIO.input(6)
        print(f"sensor output: {sensor_output}")
        if sensor_output == MODE.HIGH.value:
            print("Light detected!")
            last_notification_time = current_time
        else:
            if (current_time - last_notification_time) >= notification_interval:
                send_txt("No light detected", "Plant A has no light")
                print("No light detected - notification sent.")
                last_notification_time = current_time

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program stopped by user.")
