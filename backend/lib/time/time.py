from pytz import timezone
from datetime import datetime, timedelta, date, time as dttime
import time
from dataclasses import dataclass
from lib import log
from lib.time.timezone import india
from lib.time.exchange_time import ExchangeTime
from lib.time.time_wait import TimeWait
from lib.time.time_service import TimeService


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
            if self.__exchange_time.get_end_time() > datetime.utcnow().astimezone(india).time() > till:
                self.__logger.info("time to start working!!")
                break
            self.__logger.info(f"waiting to start curr:{datetime.utcnow().astimezone(india).time()} till:{till}!!")
            time.sleep(60)

    def wait_till_nextday(self):
        today = datetime.utcnow().astimezone(india)
        next_day = today + timedelta(days=1)
        while True:
            if datetime.utcnow().astimezone(india).date() < next_day.date():
                self.__logger.info(
                    f"waiting to next day. curr:{datetime.utcnow().astimezone(india).date()} next_day:{next_day.date()}!!")
                time.sleep(3600)
                continue
            break
        pass

