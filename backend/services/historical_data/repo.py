from typing import List
from lib.mongo_db import db
from pymongo import ReplaceOne
from lib import log
from injector import inject
from services.historical_data import HistoricalDataRepository

class Repository(HistoricalDataRepository):
    @inject
    def __init__(self, logger: log.Logger):
        self.__logger = logger

    def insert(self, token: str, period: str, data: List[dict]):
        # upsert
        for ohlc in data:
            ohlc['instrument_token'] = token

        upserts = [ReplaceOne({'instrument_token': token, 'date': ohlc['date']}, ohlc, upsert=True) for ohlc in data]
        result = db[f"ohlc_{period}"].bulk_write(upserts)


    def get_for_date(self, token: str, period: str, for_date) -> dict:
        data = list(db[f"ohlc_{period}"].find({"instrument_token": token, "date": for_date}).limit(1))
        if len(data) > 0:
            return data[0]
        return None

