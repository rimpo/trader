from kiteconnect import KiteConnect
from lib import log
from services.auth.auth import AuthService
from injector import inject
from datetime import datetime
from typing import List


class HistoricalDataService:
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
    PERIOD_1m = "minute"
    PERIOD_3m = "3minute"
    PERIOD_5m = "5minute"
    PERIOD_10m = "10minute"
    PERIOD_15m = "15minute"
    PERIOD_30m = "30minute"
    PERIOD_60m = "60minute"
    PERIOD_1d = "day"

    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def get_historical_data(self, token: int, from_date: datetime, to_date: datetime, period: str, ) -> List[dict]:
        if from_date > to_date:
            raise Exception(f"from_date > to_date")
        fmt = '%Y-%m-%d %H:%M:%S'
        return self.__kite.historical_data(
            token,
            from_date.strftime(fmt),
            to_date.strftime(fmt),
            interval=period,
            continuous=False, oi=True
        )

