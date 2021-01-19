from injector import inject
from services.strategy.signal.signals import SignalRepository, Signal, BUY_SIGNAL, SELL_SIGNAL
from datetime import datetime
from lib.mongo_db import db
from typing import Optional
from lib import log


class Repository(SignalRepository):
    @inject
    def __init__(self, logger: log.Logger):
        self.__logger = logger

    def save_signal(self, token: str, signal_type: str, date: datetime):
        db["signals"].insert_one({
            "processed": False,
            "signal": signal_type,
            "date": date,
            "instrument_token": token
        })

    def get_unprocessed_signal(self) -> Optional[Signal]:
        signal = list(db["signals"].find({"processed": False}).limit(1))
        self.__logger.info(f"found signal {signal}!!")
        if len(signal) > 0:
            return Signal(
                instrument_token=signal[0]["instrument_token"],
                processed=signal[0]["processed"],
                date=signal[0]["date"],
                signal_type=signal[0]["signal"],
                id=signal[0]["_id"],
            )
        return None

    def set_signal_processed(self, id):
        db["signals"].update_one({"_id": id}, {"$set": {"processed": True}})
