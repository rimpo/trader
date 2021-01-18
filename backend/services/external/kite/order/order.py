from lib import log
from injector import inject
from services.auth.auth import AuthService
from services.order.order import ExternalMarketOrderServiceCNC


class MarketOrderService(ExternalMarketOrderServiceCNC):
    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def buy_cnc(self, symbol: str, qty: int):
        self.__logger.warning(f"***** BUY CNC MARKET ORDER for symbol:{symbol} qty:{qty} *****")
        self.__kite.place_order(
            self.__kite.VARIETY_REGULAR,
            self.__kite.EXCHANGE_NSE,
            symbol,
            transaction_type=self.__kite.TRANSACTION_TYPE_BUY,
            quantity=qty,
            product=self.__kite.PRODUCT_CNC,
            order_type=self.__kite.ORDER_TYPE_MARKET
        )

    def sell_cnc(self, symbol: str, qty: int):
        self.__logger.warning(f"***** SELL CNC MARKET ORDER for symbol:{symbol} qty:{qty} *****")
        self.__kite.place_order(
            self.__kite.VARIETY_REGULAR,
            self.__kite.EXCHANGE_NSE,
            symbol,
            transaction_type=self.__kite.TRANSACTION_TYPE_SELL,
            quantity=qty,
            product=self.__kite.PRODUCT_CNC,
            order_type=self.__kite.ORDER_TYPE_MARKET
        )
