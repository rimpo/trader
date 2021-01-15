from lib.mongo_db import db
from datetime import datetime


class Ohlc5min(db.Document):
    token = db.IntField()
    date = db.DateTimeField(default=datetime.utcnow)
    open_price = db.FloatField()
    close_price = db.FloatField()
    high_price = db.FloatField()
    low_price = db.FloatField()
    volume = db.IntField()
    meta = {
        'indexes': [
            {'fields': ('token', 'date'), 'unique': True}
        ]
    }

