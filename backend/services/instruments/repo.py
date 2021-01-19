from lib.mongo_db import db
from injector import inject
from pymongo import ReplaceOne
from lib import log


class Repository:
    @inject
    def __init__(self, logger: log.Logger):
        self.__logger = logger

    def insert_instruments(self, instruments: dict):
        upserts = [ReplaceOne({'instrument_token': str(instrument['instrument_token'])}, instrument, upsert=True) for instrument in instruments]
        db["instruments"].insert_many(instruments)

    def get_symbol(self, token: str) -> str:
        data = db["instruments"].find_one({"instrument_token": int(token)})
        if data is not None
            return data["tradingsymbol"]
        raise Exception(f"Token not found {token}")

    def get_token(self, symbol: str) -> str:
        data = db["instruments"].find_one({"tradingsymbol": symbol})
        if data and len(list(data)) > 0:
            return str(data['instrument_token'])
        raise Exception(f"Symbol not found in instruments. {symbol}")
