from injector import inject
from kiteconnect import KiteConnect
from services.auth.auth import AuthService
from typing import List, Dict
from collections import defaultdict
from services.order.position import ExternalPositionService

class PositionService(ExternalPositionService):
    @inject
    def __init__(self, auth: AuthService):
        self.__kite = auth.get_kite()

    def get_positions_all(self) -> List[dict]:
        return self.__kite.positions()

    def __form_position_key(self, position) -> str:
        return f"{position['tradingsymbol']}-{position['exchange']}"

    def assert_position(self, position):
        """current I am unaware about the data therefore putting some checks"""
        if position["filled_quantity"] != position['quantity']:
            raise Exception(f'position incorrect. filled_quantity != quantity {position}')

    def get_open_position(self) -> Dict[str, int]:
        open_position = defaultdict(int)
        for position in self.get_positions_all():
            self.assert_position(position)
            if position['transaction_type'] == self.__kite.TRANSACTION_TYPE_BUY:
                open_position[position['tradingsymbol']] += position['filled_quantity']
            if position['transaction_type'] == self.__kite.TRANSACTION_TYPE_SELL:
                open_position[position['tradingsymbol']] += position['filled_quantity']
        return open_position
