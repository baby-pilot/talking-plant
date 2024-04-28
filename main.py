"""
execute main script here e.g. run all processes in multiple threads
"""

import threading
import time
from datetime import datetime

from light_check import check_light
from moisture_check import check_moisture
from object_detection import ObjectDetector

# from object_detection import *
from bt_speak import AlertMode, speak
from send_sms import send_txt

# from google_send_sms import send_txt as g_send_txt
import collections

event_time_dict = {}
txt_alert_dict = {
    AlertMode.NEED_DEFENSE: "It's me, plant, you gotta defend me, I'll be eaten!",
    AlertMode.NEED_UV: "Hey, it's me again, can you please move me, I need some sunshine.",
    AlertMode.NEED_WATER: "Hey this is your plant speaking, please water me.",
}
alert_q = collections.deque()

def main():
    moisture_event = threading.Event()
    light_event = threading.Event()
    intruder_event = threading.Event()

    # Initialize the moisture thread
    moisture_check_thread = threading.Thread(
        target=check_moisture, args=(moisture_event, alert_q)
    )
    moisture_check_thread.daemon = True  # run as daemon so it is stopped when main is stopped

    # Initialize the light thread
    light_check_thread = threading.Thread(
        target=check_light, args=(light_event, alert_q)
    )
    light_check_thread.daemon = True

    # Initialize Object detection thread
    intruder_detection = ObjectDetector(intruder_event)
    object_detection_thread = threading.Thread(
        target=intruder_detection.detect_objects, args=(alert_q,)
    )
    object_detection_thread.daemon = True

    # Start the threads
    moisture_check_thread.start()
    light_check_thread.start()
    object_detection_thread.start()

    try:
        while True:
            if alert_q:
                alert_mode = alert_q.popleft()
                print(alert_q)
                print("Alerting mode ", alert_mode)
                speak(alert_mode)
                send_txt(txt_alert_dict[alert_mode])
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped, shutting down...")


if __name__ == "__main__":
    main()
