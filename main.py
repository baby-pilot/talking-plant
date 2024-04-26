'''
execute main script here e.g. run all processes in multiple threads
'''
import threading
import time

from light_check import check_light
from moisture_check import check_moisture
from object_detection import *
from bt_speak import AlertMode, speak
import collections

def alert_manager(alert_mode, event, alert_q, channel_free_flag):
    """
    Thread function to manage alerts for specific events
    The thread waits on the specified event to be set and immediately speaks the alert
    """
    while True:
        event.wait()
        channel_free_flag.wait()  # if set, no current msg, if unset, currently playing a message
        channel_free_flag.clear()  # signals a message is currently played
        speak(alert_mode)
        event.clear()
        channel_free_flag.set()  # signal that channel is free for next message

        
def main():
    moisture_event = threading.Event()
    light_event = threading.Event()
    alert_q = collections.deque()  # thread safe
    event_dict = {
        AlertMode.NEED_UV: moisture_event,
        AlertMode.NEED_WATER: light_event
    }

    # Initialize the moisture thread
    moisture_check_thread = threading.Thread(target=check_moisture, args=(moisture_event))
    moisture_check_thread.daemon = True

    # Initialize the light thread
    light_check_thread = threading.Thread(target=check_light, args=(light_event))
    light_check_thread.daemon = True

    # Start the threads
    moisture_check_thread.start()
    light_check_thread.start()

    # Start alert manager threads
    for alert_mode, event in event_dict.items():
        threading.Thread(target=alert_manager, args=(alert_mode, event), daemon=True).start()

    ## ----- with alert manager thread, below is unnecessary ----- ##
    
    # check event signals and play messages
    # while True:
    #     if alert_q:
    #         alert: AlertMode = alert_q.popleft()
    #         event = event_dict[alert]
    #         if event.is_set():
    #             speak(alert)
    #             event.clear()
    #     time.sleep(2)


if __name__ == '__main__':
    main()