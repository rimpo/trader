from datetime import datetime, timedelta
from typing import  Protocol

from lib.time.timezone import india, germany

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

