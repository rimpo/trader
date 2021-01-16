from typing import List
from lib.mongo_db import db

class Repository:
    def __init__(self):
        pass

    def insert(self, token: int, period: str, data: List[dict]):
        db[f"ohlc_{token}_{period}"].insert_many(data)
