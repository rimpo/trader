from injector import inject
from services.strategy.signal.signals import SignalRepository, Signal, BUY_SIGNAL, SELL_SIGNAL
from datetime import datetime
from lib.mongo_db import db
from typing import Optional


class Repository(SignalRepository):
    def __init__(self):
        pass

    def save_signal(self, token: str, signal_type: str, date: datetime):
        db["signal"].insert_one({
            "processed": False,
            "signal_type": signal_type,
            "date": date,
            "instrument_token": token
        })

    def get_unprocessed_signal(self, token: int) -> Optional[Signal]:
        signal = list(db["signal"].find({"processed": False}).limit(1))
        if len(signal) > 0:
            return Signal(
                instrument_token=signal[0]["instrument_token"],
                processed=signal[0]["processed"],
                date=signal[0]["date"],
                signal_type=signal[0]["signal_type"],
                id=signal[0]["_id"],
            )
        return None

    def set_signal_processed(self, id):
        db["signal"].update_one({"_id": id}, {"processed": True})
