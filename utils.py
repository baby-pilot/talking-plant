from datetime import datetime


class IntervalExponentialBackOff:
    """
    Implements a class for exponential backoff,
    allowing each alert to be spaced out with an exponential backoff
    """

    def __init__(self, base_time=10):
        self._counter = 0
        self._base_time = base_time
        self._last_alert = datetime.min

    def reset(self):
        self._counter = 0
        self._last_alert = datetime.min

    def set(self):
        self._counter += 1
        self._last_alert = datetime.now()

    def back_off_passed(self) -> bool:
        time_since_last_alert = (datetime.now() - self._last_alert).total_seconds()
        back_off_time = 5**self._counter * self._base_time  # 10 seconds base time
        return time_since_last_alert >= back_off_time
