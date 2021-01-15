from lib.mongo_db import db


class AuthModel(db.Document):
    request_token = db.StringField()
    access_token = db.StringField()
