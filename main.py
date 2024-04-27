'''
execute main script here e.g. run all processes in multiple threads
'''
import threading
import time
from datetime import datetime

from light_check import check_light
from moisture_check import check_moisture
# from object_detection import *
from bt_speak import AlertMode, speak
import collections

event_time_dict = {}
alert_q = collections.deque()

def alert_manager(alert_q, moisture_event, light_event):
    while True:
        if alert_q:
            alert_mode = alert_q.popleft()  # Retrieve the next alert and its timestamp

            # Check if we should play this alert, or skip based on last played time
            # use alert count to generate exponential back-off
            last_time, alert_count = event_time_dict.get(alert_mode, (datetime.min, 0))
            time_since_last_alert = (datetime.now() - last_time).total_seconds()
            
            # Exponential back-off calculation
            back_off_time = 10 ** alert_count * 10  # 10 seconds base time
            print(last_time, alert_count)
            print(time_since_last_alert, back_off_time)
            if time_since_last_alert >= back_off_time:
                    print("Alerting mode ", alert_mode)
                    speak(alert_mode)
                    event_time_dict[alert_mode] = (datetime.now(), alert_count + 1)  # Update last alert time
                    print(event_time_dict)
            else:
                print(f"Skipping {alert_mode} due to back off policy.")
        else:
            # reset the back-off if corrective action has been taken
            if not moisture_event.is_set():
                if AlertMode.NEED_WATER in event_time_dict:
                    print("clearning event_time_dict", moisture_event.is_set())
                    del event_time_dict[AlertMode.NEED_WATER]
            if not light_event.is_set():
                if AlertMode.NEED_UV in event_time_dict:
                    del event_time_dict[AlertMode.NEED_UV]

def sensor_check(sensor_event, alert_q, alert_type):
    while True:
        sensor_event.wait()
        alert_q.append(alert_type)  # Append new alert to the queue if condition is met
        # sensor_event.clear()
        
def main():
    moisture_event = threading.Event()
    light_event = threading.Event()

    # Initialize the moisture thread
    moisture_check_thread = threading.Thread(target=check_moisture, args=(moisture_event,))
    moisture_check_thread.daemon = True

    # Initialize the light thread
    light_check_thread = threading.Thread(target=check_light, args=(light_event,))
    light_check_thread.daemon = True

    # Start the threads
    moisture_check_thread.start()
    light_check_thread.start()

    # Threads for checking sensors
    threading.Thread(target=sensor_check, args=(moisture_event, alert_q, AlertMode.NEED_WATER), daemon=True).start()
    threading.Thread(target=sensor_check, args=(light_event, alert_q, AlertMode.NEED_UV), daemon=True).start()


    # Single alert manager thread
    threading.Thread(target=alert_manager, args=(alert_q, moisture_event, light_event), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped, shutting down...")

if __name__ == '__main__':
    main()