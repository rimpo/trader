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

    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def get_historical_data(self, token: int, period: str, from_date: datetime, to_date: datetime) -> List[dict]:
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

