from kiteconnect import KiteConnect
from lib import log
from services.auth.auth import AuthService
from injector import inject
from datetime import datetime, timedelta
from typing import List
import time
from services.historical_data.historical_data import ExternalHistoricalDataService


class HistoricalDataService(ExternalHistoricalDataService):
    """
    Historical data limits
    minute : 60 days
    3minute : 100 days
    5minute : 100 days
    10minute : 100 days
    15minute : 200 days
    30minute : 200 days
    60minute : 400 days
    day : 2000 days
    """
    INTERVAL = {
        # 1: "minute", NOTE: dont want to support 1 minute data
        3: "3minute",
        5: "5minute",
        10: "10minute",
        15: "15minute",
        30: "30minute",
        60: "60minute",
        86400: "day",
    }

    FORMAT = '%Y-%m-%d %H:%M:%S'

    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def get_historical_data(self, token: int, interval: int, from_date: datetime, to_date: datetime) -> List[dict]:
        if from_date > to_date:
            raise Exception(f"from_date > to_date")
        return self.__kite.historical_data(
            token,
            from_date.strftime(self.FORMAT),
            to_date.strftime(self.FORMAT),
            interval=self.INTERVAL[interval],
            continuous=False, oi=True
        )

    def get_historical_data_wait(self, token: int, date: datetime, interval: int, sleep_seconds: int):
        from_date = date
        to_date = date + timedelta(minutes=1)  # 1 minute data will not work due the granularity is minute here
        while True:
            data = self.__kite.historical_data(
                token,
                from_date.strftime(self.FORMAT),
                to_date.strftime(self.FORMAT),
                interval=self.INTERVAL[interval],
                continuous=False, oi=True
            )
            if len(data) > 1:
                raise Exception("Expecting only 1 record got more than 1 historical data")
            if len(data) == 0:
                raise Exception("Expecting only 1 record got 0. Should not be possible")
            self.__logger.debug(f"Yay! data arrived:{data} :)")
            return data[0]
