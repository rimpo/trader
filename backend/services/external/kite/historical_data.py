from kiteconnect import KiteConnect
from lib import log

class HistoricalData:
    def __init__(self, logger: log.Logger, kite: KiteConnect):
        self.__kite = kite
