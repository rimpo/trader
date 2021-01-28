from datetime import datetime, date
from typing import Protocol
from lib.time.timezone import india, germany


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
