from services.external.kite.historical_data import  HistoricalDataService as ExternalHistoricalDataService
from injector import inject
from typing import Protocol, List
from datetime import datetime


class HistoricalDataRepository(Protocol):
    def insert(self, token: int, period: str, data: List[dict]):
        pass

    def get_for_date(self, token: int, period: str, for_date):
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

    def download_and_save(self, token: int, period: str, from_date: datetime, to_date: datetime):
        data = self.__external_historical_data_service.get_historical_data(token, period, from_date, to_date)
        self.__repository.insert(token, period, data)

    def get_for_date(self, token: int, period: str, for_date) -> dict:
        """for_date needs to be in UTC"""
        return self.__repository.get_for_date(token, period, for_date)
