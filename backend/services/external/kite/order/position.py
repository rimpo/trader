from injector import inject
from services.auth.auth import AuthService
from typing import List, Dict
from collections import defaultdict
from services.order.position import ExternalPositionService
from lib import log


class PositionService(ExternalPositionService):
    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def get_positions_all(self) -> List[dict]:
        return self.__kite.positions()

    def __form_position_key(self, position) -> str:
        return f"{position['tradingsymbol']}-{position['exchange']}"

    def assert_position(self, position):
        """current I am unaware about the data therefore putting some checks"""
        if position["filled_quantity"] != position['quantity']:
            raise Exception(f'position incorrect. filled_quantity != quantity {position}')

    def get_open_position(self) -> Dict[int, dict]:
        """
        return { 975873: {'tradingsymbol': 'ZEEL', 'exchange': 'NSE', 'instrument_token': 975873, 'product': 'CNC',
         'quantity': 0, 'overnight_quantity': 0, 'multiplier': 1, 'average_price': 0, 'close_price': 0,
         'last_price': 220.65, 'value': 0.25, 'pnl': 0.25, 'm2m': 0.25, 'unrealised': 0.25, 'realised': 0, '
         buy_quantity': 5, 'buy_price': 220.25, 'buy_value': 1101.25, 'buy_m2m': 1101.25, 'sell_quantity': 5,
        'sell_price': 220.3, 'sell_value': 1101.5, 'sell_m2m': 1101.5, 'day_buy_quantity': 5,
         'day_buy_price': 220.25, 'day_buy_value': 1101.25, 'day_sell_quantity': 5, 'day_sell_price': 220.3,
         'day_sell_value': 1101.5}}
         """
        positions = self.__kite.positions()
        open_position = defaultdict(dict)
        for position in positions['net']:
            open_position[position['instrument_token']] = position
        return open_position
