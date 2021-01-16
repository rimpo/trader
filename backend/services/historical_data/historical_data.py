from services.external.kite.historical_data import  HistoricalDataService as ExternalHistoricalDataService
from injector import inject
from typing import Protocol, List
from datetime import datetime


class HistoricalDataRepository(Protocol):
    def insert(self, token: int, period: str, data: List[dict]):
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

    def download_and_save(self, token: int, from_date: datetime, to_date: datetime, period: str):
        data = self.__external_historical_data_service.get_historical_data(token, from_date, to_date, period)
        self.__repository.insert(token, period, data)
