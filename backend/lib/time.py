from pytz import timezone
from datetime import datetime, timedelta
from pytimeparse import parse
from typing import List, Tuple, Protocol
import time


india = timezone('Asia/Kolkata')
germany = timezone('Europe/Berlin')

class TimeService(Protocol):
    def __init__(self):
        pass

    def get_current_time(self):
        pass


class IndiaTimeService(TimeService):
    def __init__(self):
        pass

    def get_current_time(self):
        return datetime.utcnow().astimezone(india)


class GermanyTimeService(TimeService):
    def __init__(self):
        pass

    def get_current_time(self):
        return datetime.utcnow().astimezone(germany)

class DummyTimeService(TimeService):
        def __init__(self, start_time: datetime, interval: int):
            self.__curr_time = start_time
            self.__interval = interval

        def get_current_time(self):
            self.__curr_time += timedelta(minutes=self.__interval)
            return self.__curr_time


class ExchangeTime(Protocol):
    def get_start_time(self):
        pass

    def get_end_time(self):
        pass


class NSEExchangeTime(ExchangeTime):
    def get_start_time(self):
        return datetime.utcnow().astimezone(india).replace(hour=9, minute=15, second=0, microsecond=0).time()

    def get_end_time(self):
        return datetime.utcnow().astimezone(india).replace(hour=15, minute=30, second=0, microsecond=0).time()


class DummyExchangeTime(ExchangeTime):
    def get_start_time(self):
        return datetime.utcnow().astimezone(germany).replace(hour=9, minute=15, second=0, microsecond=0).time()

    def get_end_time(self):
        return datetime.utcnow().astimezone(germany).replace(hour=15, minute=30, second=0, microsecond=0).time()


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

class TimeRange:
    VALID_INTERVAL = {
        3: [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57],
        5: [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
        10: [0, 10, 20, 30, 40, 50],
        15: [0, 15, 30, 45],
        30: [15, 45],
        60: [15, ]
    }

    def __init__(self, interval: int, time_service: TimeService, exchange_time: ExchangeTime, time_wait: TimeWait):
        if interval not in self.VALID_INTERVAL:
            raise Exception(f"Invalid interval minutes {interval}")
        self.__interval = interval
        self.__time_service = time_service
        self.__exchange_time = exchange_time
        self.__time_wait = time_wait

    def get_next(self):
        previous_time = None
        while True:
            curr_time = self.__time_service.get_current_time()
            curr_time = curr_time.replace(second=0, microsecond=0)
            if curr_time.minute in self.VALID_INTERVAL[self.__interval]:
                actual_time = curr_time - timedelta(minutes=self.__interval)
                if previous_time and previous_time == actual_time:
                    # to avoid multiple time in same minute
                    self.__time_wait.wait()
                    continue
                if self.__exchange_time.get_start_time() <= actual_time.time() < self.__exchange_time.get_end_time():
                    # exchange is open at that time
                    previous_time = actual_time
                    yield actual_time
            self.__time_wait.wait()
