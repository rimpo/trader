from typing import List
from lib.mongo_db import db
from pymongo import ReplaceOne
from lib import log
from injector import inject
from services.historical_data import HistoricalDataRepository
from datetime import datetime
import pymongo

class Repository(HistoricalDataRepository):
    @inject
    def __init__(self, logger: log.Logger):
        self.__logger = logger

    def insert_one(self, token: str, interval: int, data: dict):
        data['instrument_token'] = token
        result = db[f"ohlc_{interval}"].replace_one({'instrument_token': token, 'date': data['date']}, data, upsert=True)

    def insert(self, token: str, interval: int, data: List[dict]):

        # upsert
        for ohlc in data:
            ohlc['instrument_token'] = token

        upserts = [ReplaceOne({'instrument_token': token, 'date': ohlc['date']}, ohlc, upsert=True) for ohlc in data]
        result = db[f"ohlc_{interval}"].bulk_write(upserts)

    def get_candle(self, token: str, interval: str, for_date) -> dict:
        data = list(db[f"ohlc_{interval}"].find({"instrument_token": token, "date": for_date}).limit(1))
        if len(data) > 0:
            return data[0]
        return None

    def get_candles(self, token: str, interval: int, no_of_candles: int, from_date: datetime):
        cursor_candles = db[f"ohlc_{interval}"].find({"instrument_token": token, }).sort("date", pymongo.DESCENDING).limit(no_of_candles)
        if cursor_candles:
            candles = list(cursor_candles)
            if len(candles) == no_of_candles:
                return candles
        raise Exception(f"Requested number of candles don't exist. token:{token} interval:{interval}min requested:{no_of_candles}")