from typing import Protocol
from injector import inject
from lib import log
from services.instruments import InstrumentService


class ExternalMarketOrderServiceCNC(Protocol):
    def buy_cnc(self, exchange: str, symbol: str, qty: int):
        pass

    def sell_cnc(self, exchange: str, symbol: str, qty: int):
        pass


class MarketOrderServiceCNC:
    @inject
    def __init__(self, logger: log.Logger, external_order_service: ExternalMarketOrderServiceCNC):
        self.__logger = logger
        self.__external_order_service = external_order_service

    def buy(self, exchange: str, symbol: str, qty: int):
        self.__external_order_service.buy_cnc(exchange, symbol, qty)

    def sell(self, exchange: str, symbol: str, qty: int):
        self.__external_order_service.sell_cnc(exchange, symbol, qty)


class ExternalMISMarketOrderService(Protocol):
    def buy_cnc(self, exchange: str, symbol: str, qty: int):
        pass

    def sell_cnc(self, exchange: str, symbol: str, qty: int):
        pass


class MISMarketOrderService:
    @inject
    def __init__(self, logger: log.Logger, external_order_service: ExternalMISMarketOrderService):
        self.__logger = logger
        self.__external_order_service = external_order_service

    def buy(self, exchange: str, symbol: str, qty: int):
        self.__external_order_service.buy_mis(exchange, symbol, qty)

    def sell(self, exchange: str, symbol: str, qty: int):
        self.__external_order_service.sell_mis(exchange, symbol, qty)





