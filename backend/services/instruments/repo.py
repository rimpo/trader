from lib.mongo_db import db
from injector import inject


class Repository:
    @inject
    def __init__(self):
        pass

    def insert_instruments(self, instruments: dict):
        for instrument in instruments:
            instruments["_id"] = instrument['instrument_token']
        db["instruments"].insert_many(instruments)

    def get_symbol(self, token: int) -> str:
        data = db["instruments"].find_one({"_id": token})
        if list(data) > 0:
            return data['tradingsymbol']
        raise Exception(f"Token not found in instruments. {token}")

    def get_token(self, symbol: str) -> str:
        data = db["instruments"].find_one({"tradingsymbol": symbol})
        if list(data) > 0:
            return data['instrument_token']
        raise Exception(f"Symbol not found in instruments. {symbol}")
