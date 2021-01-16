from injector import inject
from services.auth.auth import AuthService


class OrderService:
    @inject
    def __init__(self, auth: AuthService):
        self.__kite = auth.get_kite()

    def buy_market_order_cnc(self, symbol: str, qty: int):
        self.__kite.place_order(
            self.__kite.VARIETY_REGULAR,
            self.__kite.EXCHANGE_NSE,
            symbol,
            transaction_type=self.__kite.TRANSACTION_TYPE_BUY,
            quantity=qty,
            product=self.__kite.PRODUCT_CNC,
            order_type=self.__kite.ORDER_TYPE_MARKET
        )

    def sell_market_order_cnc(self, symbol: str, qty: int):
        self.__kite.place_order(
            self.__kite.VARIETY_REGULAR,
            self.__kite.EXCHANGE_NSE,
            symbol,
            transaction_type=self.__kite.TRANSACTION_TYPE_SELL,
            quantity=qty,
            product=self.__kite.PRODUCT_CNC,
            order_type=self.__kite.ORDER_TYPE_MARKET
        )
