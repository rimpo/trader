from kiteconnect import KiteConnect
from lib import log

class InstrumentService:
    def __init__(self, logger: log.Logger, kite: KiteConnect):
        self.__logger = logger
        self.__kite = kite

    def get_instruments(self) -> dict:
        return self.__kite.instruments()

