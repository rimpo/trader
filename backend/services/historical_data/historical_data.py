from injector import inject
from typing import Protocol, List
from datetime import datetime
import time


class ExternalHistoricalDataService(Protocol):
    def get_historical_data(self, token: int, interval: int, from_date: datetime, to_date: datetime) -> List[dict]:
        pass

    def get_historical_data_wait(self, token: int, date: datetime, interval: int, sleep_seconds: int):
        pass


class HistoricalDataRepository(Protocol):
    def insert(self, token: int, interval: int, data: List[dict]):
        pass

    def get_candle(self, token: int, interval: int, for_date: datetime):
        pass

    def get_candles(self, token: str, interval: int, no_of_candles: int, from_date: datetime):
        pass


class HistoricalDataService:
    PERIOD_1m = "minute"
    PERIOD_3m = "3minute"
    PERIOD_5m = "5minute"
    PERIOD_10m = "10minute"
    PERIOD_15m = "15minute"
    PERIOD_30m = "30minute"
    PERIOD_60m = "60minute"
    PERIOD_1d = "day"

    @inject
    def __init__(self, external_historical_data_service: ExternalHistoricalDataService, repository: HistoricalDataRepository):
        self.__external_historical_data_service = external_historical_data_service
        self.__repository = repository

    def download_and_save(self, token: int, interval: int, from_date: datetime, to_date: datetime):
        data = self.__external_historical_data_service.get_historical_data(token, interval, from_date, to_date)
        self.__repository.insert(token, interval, data)

    def wait_download_and_save(self, token: int, date: datetime, interval: int, sleep_seconds: int = 15):
        data = self.__external_historical_data_service.get_historical_data_wait(token, date, interval, sleep_seconds)
        self.__repository.insert(token, interval, data)

    def get_candle(self, token: int, interval: str, for_date: datetime) -> dict:
        """for_date needs to be in UTC"""
        return self.__repository.get_candle(token, interval, for_date)

    def get_candle_wait(self, token: int, interval: str, for_date: datetime, sleep_seconds: int = 15) -> dict:
        while True:
            data = self.__repository.get_candle(token, interval, for_date)
            if data is not None:
                return data
            time.sleep(sleep_seconds)

    def get_candles(self, token: str, interval: int, no_of_candles: int, from_date: datetime) -> List[dict]:
        return self.__repository.get_candles(token, interval, no_of_candles, from_date)
