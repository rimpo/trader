from typing import Protocol
from injector import inject
from lib import log
from services.instruments import InstrumentService


class ExternalMarketOrderServiceCNC(Protocol):
    def buy_cnc(self, symbol: str, qty: int):
        pass

    def sell_cnc(self, symbol: str, qty: int):
        pass


class MarketOrderServiceCNC:
    @inject
    def __init__(self, logger: log.Logger, external_order_service: ExternalMarketOrderServiceCNC, instrument_service: InstrumentService):
        self.__logger = logger
        self.__external_order_service = external_order_service
        self.__instrument_service = instrument_service

    def buy(self, token: str, qty: int):
        symbol = self.__instrument_service.get_symbol(token)
        self.__external_order_service.buy_cnc(symbol, qty)

    def sell(self, token: str, qty: int):
        symbol = self.__instrument_service.get_symbol(token)
        self.__external_order_service.buy_cnc(symbol, qty)


class ExternalMISMarketOrderService(Protocol):
    def buy_cnc(self, symbol: str, qty: int):
        pass

    def sell_cnc(self, symbol: str, qty: int):
        pass


class MISMarketOrderService:
    @inject
    def __init__(self, logger: log.Logger, external_order_service: ExternalMISMarketOrderService, instrument_service: InstrumentService):
        self.__logger = logger
        self.__external_order_service = external_order_service
        self.__instrument_service = instrument_service

    def buy(self, token: str, qty: int):
        symbol = self.__instrument_service.get_symbol(token)
        self.__external_order_service.buy_mis(symbol, qty)

    def sell(self, token: str, qty: int):
        symbol = self.__instrument_service.get_symbol(token)
        self.__external_order_service.buy_mis(symbol, qty)
