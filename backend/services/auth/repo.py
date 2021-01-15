from lib.mongo_db import db


class Repository:
    def create_auth(self, request_token: str, access_token: str):
        db["auth"].replace_one({"_id": 1}, {"_id": 1, "request_token": request_token, "access_token": access_token}, upsert=True)

    def get_auth(self) -> dict:
        return db["auth"].find_one({"_id": 1})
