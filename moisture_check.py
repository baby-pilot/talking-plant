import RPi.GPIO as GPIO
import time
from send_sms import send_txt
from bt_speak import speak, AlertMode

# Set up GPIO pin
sensor_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN, initial=GPIO.LOW)

try:
    while True:
        if GPIO.input(sensor_pin) == GPIO.HIGH:
            # Soil is dry! Need watering.
            speak(AlertMode.NEED_WATER)
        else:
            print("Checked soil. Is wet, no need watering.")
        time.sleep(10)
except KeyboardInterrupt:
    # clean up resources used to avoid damage to RPi
    GPIO.cleanup()