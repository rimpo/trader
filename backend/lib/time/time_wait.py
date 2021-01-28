from typing import Protocol
import time


class TimeWait(Protocol):
    def wait(self):
        time.sleep(0.1)
        pass


class TimeSleepWait(TimeWait):
    def __init__(self, seconds: int):
        self.__seconds = seconds

    def wait(self):
        time.sleep(self.__seconds)


class DummySleepWait(TimeWait):
    def wait(self):
        pass