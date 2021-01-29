from injector import inject
from services.auth.auth import AuthService
from typing import List, Dict
from collections import defaultdict
from services.order.holding import ExternalHoldingService
from lib import log


class HoldingService(ExternalHoldingService):
    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()

    def get_holdings(self) -> List[dict]:
        return self.__kite.holdings()

    def __form_holding_key(self, position) -> str:
        return f"{position['tradingsymbol']}-{position['exchange']}"

    def assert_holding(self, position):
        """current I am unaware about the data therefore putting some checks"""
        if position["filled_quantity"] != position['quantity']:
            raise Exception(f'position incorrect. filled_quantity != quantity {position}')

    def get_open_holding(self) -> Dict[int, dict]:
        holdings = self.__kite.holdings()
        open_holding = defaultdict(dict)
        for holding in holdings:
            open_holding[holding['instrument_token']] = holding
        return open_holding

