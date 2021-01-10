from kiteconnect import KiteTicker
from lib import log


class TickService:
    def __init__(self, logger: log.Logger, api_key: str, access_token: str):
        self.__kite_ticker = KiteTicker(api_key, access_token)

    def on_ticks(self, ws, ticks):
        pass

    def start(self):
        self.__kite_ticker.connect()
