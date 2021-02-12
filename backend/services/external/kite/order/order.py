from lib import log
from injector import inject
from services.auth.auth import AuthService
from services.order.order import ExternalMarketOrderServiceCNC, ExternalMISMarketOrderService


class MarketOrderService(ExternalMarketOrderServiceCNC, ExternalMISMarketOrderService):
    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def buy_cnc(self, exchange: str, symbol: str, qty: int):
        self.__kite.place_order(
            self.__kite.VARIETY_REGULAR,
            exchange,
            symbol,
            transaction_type=self.__kite.TRANSACTION_TYPE_BUY,
            quantity=qty,
            product=self.__kite.PRODUCT_CNC,
            order_type=self.__kite.ORDER_TYPE_MARKET
        )
        self.__logger.warning(f"***** BUY CNC MARKET ORDER for exchange:{exchange} symbol:{symbol} qty:{qty} *****")

    def sell_cnc(self, exchange: str, symbol: str, qty: int):
        self.__kite.place_order(
            self.__kite.VARIETY_REGULAR,
            exchange,
            symbol,
            transaction_type=self.__kite.TRANSACTION_TYPE_SELL,
            quantity=qty,
            product=self.__kite.PRODUCT_CNC,
            order_type=self.__kite.ORDER_TYPE_MARKET
        )
        self.__logger.warning(f"***** SELL CNC MARKET ORDER for exchange:{exchange} symbol:{symbol} qty:{qty} *****")

    def buy_mis(self, exchange: str, symbol: str, qty: int):
        order = self.__kite.place_order(
            self.__kite.VARIETY_REGULAR,
            exchange,
            symbol,
            transaction_type=self.__kite.TRANSACTION_TYPE_BUY,
            quantity=int(qty),
            product=self.__kite.PRODUCT_MIS,
            order_type=self.__kite.ORDER_TYPE_MARKET
        )
        self.__logger.warning(f"***** BUY MIS MARKET ORDER for exchange:{exchange} symbol:{symbol} qty:{qty} order:{order}*****")

    def sell_mis(self, exchange: str, symbol: str, qty: int):
        order = self.__kite.place_order(
            self.__kite.VARIETY_REGULAR,
            exchange,
            symbol,
            transaction_type=self.__kite.TRANSACTION_TYPE_SELL,
            quantity=int(qty),
            product=self.__kite.PRODUCT_MIS,
            order_type=self.__kite.ORDER_TYPE_MARKET
        )
        self.__logger.warning(f"***** SELL MIS MARKET ORDER for exchange:{exchange} symbol:{symbol} qty:{qty} order:{order}*****")
