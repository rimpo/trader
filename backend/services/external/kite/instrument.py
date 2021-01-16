from kiteconnect import KiteConnect
from lib import log
from services.auth.auth import AuthService
from injector import inject


class InstrumentService:
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def get_instruments(self) -> dict:
        return self.__kite.instruments(exchange=self.__kite.EXCHANGE_NSE)