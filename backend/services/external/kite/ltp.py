from kiteconnect import KiteConnect
from lib import log
from services.auth.auth import AuthService
from typing import List


class LTPService:
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def get_ltp(self, exchange: str, symbols: List[str]) -> dict:
        return self.__kite.ltp(instruments=[f"{exchange}:{symbol}" for symbol in symbols])
