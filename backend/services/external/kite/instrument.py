from kiteconnect import KiteConnect
from lib import log
from services.auth.auth import AuthService
from injector import inject
from services.instruments import ExternalInstrumentService
from typing import List


class InstrumentService(ExternalInstrumentService):
    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def get_instruments(self) -> dict:
        return self.__kite.instruments(exchange=self.__kite.EXCHANGE_NSE)

    def get_ltp(self, symbols: List[str]):
        return self.__kite.ltp([f"{self.__kite.EXCHANGE_NSE}:{symbol}" for symbol in symbols])
