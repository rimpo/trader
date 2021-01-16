import pymongo
from typing import List
from lib.mongo_db import db

class Repository:
    def get_candles(self, token: int, period: str, length: int) -> List[dict]:
        return list(db[f"ohlc_{token}_{period}"].find().sort("date", pymongo.DESCENDING).limit(length))

    def write_candles(self, token: int, period: str, data: dict):
        pass
