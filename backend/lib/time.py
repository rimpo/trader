from pytz import timezone
from datetime import datetime, timedelta,time
from pytimeparse import parse
from typing import List, Tuple

india = timezone('Asia/Kolkata')

class TimeService:
    def __init__(self):
        pass


def get_today_exchange_start_time():
    return datetime.utcnow().astimezone(india).replace(hour=9, minute=15, second=0, microsecond=0)


def get_today_exchange_end_time():
    return datetime.utcnow().astimezone(india).replace(hour=15, minute=30, second=0, microsecond=0)


def get_interval_range(interval: int) -> List[Tuple[datetime, datetime]]:
    result = []
    start_time = get_today_exchange_start_time()
    while start_time <= get_today_exchange_end_time():
        end_time = start_time + timedelta(minutes=interval)

        if end_time > get_today_exchange_end_time():
            # interval like 30 minutes and 1hour have last candle of 15min
            end_time = get_today_exchange_end_time()

        result.append((start_time, end_time))
        start_time += timedelta(minutes=interval)
    return result


class IntervalRange:
    VALID_INTERVAL = [3, 5, 10, 15, 30, 60]
    """ take intervals in minute """
    def __init__(self, interval_minutes: int):
        if interval_minutes not in self.VALID_INTERVAL:
            raise Exception(f"Invalid interval minutes {interval_minutes}")
        self.__interval_minutes = interval_minutes
        self.__interval_ranges = get_interval_range(interval_minutes)

    def get_range(self, curr_time) -> Tuple[datetime, datetime]:
        for (start_time, end_time) in self.__interval_ranges:
            yield start_time, end_time

    def get_todays_first(self, curr_time) -> Tuple[datetime, datetime]:

        for (start_time, end_time) in self.__interval_ranges:
            yield start_time, end_time

