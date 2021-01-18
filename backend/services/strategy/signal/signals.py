from typing import Protocol
from datetime import datetime
import enum
from dataclasses import dataclass
from injector import inject


BUY_SIGNAL = "BUY"
SELL_SIGNAL = "SELL"


@dataclass(frozen=True)
class Signal:
    id: str
    signal_type: str
    instrument_token: str
    date: datetime
    processed: bool

    def is_buy_signal(self):
        return self.signal_type == BUY_SIGNAL


class SignalRepository:
    def save_signal(self, token: str, signal_type: str, date: datetime):
        pass

    def get_unprocessed_signal(self):
        pass


class SignalService:
    @inject
    def __init__(self, repository: SignalRepository):
        self.__repository = repository

    def __save_signal(self, token: str, signal_type: str, date: datetime):
        self.__repository.save_signal(token, signal_type, date)

    def save_buy_signal(self, token, date: datetime):
        self.__save_signal(token, BUY_SIGNAL, date)

    def save_sell_signal(self, token, date: datetime):
        self.__save_signal(token, SELL_SIGNAL, date)

    def get_unprocessed_signal(self) -> Signal:
        return self.__repository.get_unprocessed_signal()

    def set_signal_processed(self, id):
        self.__repository.set_signal_processed(id)

