from typing import Protocol
from injector import inject
from lib import log


class ExternalMarketOrderServiceCNC(Protocol):
    def buy_cnc(self, symbol: str, qty: int):
        pass

    def sell_cnc(self, symbol: str, qty: int):
        pass


class MarketOrderServiceCNC:
    @inject
    def __init__(self, logger: log.Logger, external_order_service: ExternalMarketOrderServiceCNC):
        self.__logger = logger
        self.__external_order_service = external_order_service

    def buy(self, symbol: str, qty: int):
        self.__external_order_service.buy_cnc(symbol, qty)

    def sell(self, symbol: str, qty: int):
        self.__external_order_service.buy_cnc(symbol, qty)

