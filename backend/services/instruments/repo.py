from lib.mongo_db import db
from injector import inject
from pymongo import ReplaceOne


class Repository:
    @inject
    def __init__(self):
        pass

    def insert_instruments(self, instruments: dict):
        upserts = [ReplaceOne({'instrument_token': instrument['instrument_token']}, instrument, upsert=True) for instrument in instruments]
        db["instruments"].insert_many(instruments)

    def get_symbol(self, token: int) -> str:
        data = db["instruments"].find_one({"instrument_token": token})
        if len(list(data)) > 0:
            return data['tradingsymbol']
        raise Exception(f"Token not found in instruments. {token}")

    def get_token(self, symbol: str) -> str:
        data = db["instruments"].find_one({"tradingsymbol": symbol})
        if data and len(list(data)) > 0:
            return data['instrument_token']
        raise Exception(f"Symbol not found in instruments. {symbol}")
