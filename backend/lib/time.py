from pytz import timezone
from datetime import datetime, timedelta, date, time as dttime
from pytimeparse import parse
from typing import List, Tuple, Protocol
import time
from dataclasses import dataclass
from injector import inject
from lib import log


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

    def is_exchange_open(self):
        pass


class NSEExchangeTime(ExchangeTime):
    def get_start_time(self):
        return datetime.utcnow().astimezone(india).replace(hour=9, minute=15, second=0, microsecond=0).time()

    def get_end_time(self):
        return datetime.utcnow().astimezone(india).replace(hour=15, minute=30, second=0, microsecond=0).time()

    def __is_today_holiday(self):
        return datetime.utcnow().astimezone(india).date in [
            date(2021, 1, 26),
            date(2021, 3, 11),
            date(2021, 3, 29),
            date(2021, 4, 2),
            date(2021, 4, 14),
            date(2021, 4, 21),
            date(2021, 5, 13),
            date(2021, 7, 21),
            date(2021, 8, 19),
            date(2021, 9, 10),
            date(2021, 10, 15),
            date(2021, 11, 4),
            date(2021, 11, 5),
            date(2021, 11, 19),
        ]

    def is_exchange_open(self):
        # TODO: Add holiday calendar of NSE
        return datetime.utcnow().astimezone(india).weekday() and not self.__is_today_holiday()


class DummyExchangeTime(ExchangeTime):
    def get_start_time(self):
        return datetime.utcnow().astimezone(germany).replace(hour=9, minute=15, second=0, microsecond=0).time()

    def get_end_time(self):
        return datetime.utcnow().astimezone(germany).replace(hour=15, minute=30, second=0, microsecond=0).time()

    def is_exchange_open(self):
        return True


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


@dataclass(frozen=True)
class ExchangeClosedToday(Exception):
    message: str

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

            if not self.__exchange_time.is_exchange_open():
                raise ExchangeClosedToday(message=f"{curr_time.date()} exchange closed today wholeday")

            if curr_time.time() > dttime(16,15):
                raise ExchangeClosedToday(message=f"{curr_time.date()} exchange is closed now.")

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


class WaitForExchangeOpenTime:
    def __init__(self, logger: log.Logger, exchange_time: ExchangeTime):
        self.__exchange_time = exchange_time
        self.__logger = logger

    def wait_till(self, till: time):
        while True:
            if not self.__exchange_time.is_exchange_open():
                self.__logger.info("exchange is closed today!. sleeping for 1 hour")
                time.sleep(3600)
            if datetime.utcnow().astimezone(india).time() > till:
                self.__logger.info("time to start working!!")
                break
            self.__logger.info(f"waiting to start curr:{datetime.utcnow().astimezone(india).time()} till:{till}!!")
            time.sleep(60)
