from injector import inject
from services.auth.auth import AuthService
from typing import List, Dict
from collections import defaultdict
from services.order.position import ExternalPositionService, OpenPosition
from lib import log


class PositionService(ExternalPositionService):
    @inject
    def __init__(self, logger: log.Logger, auth: AuthService):
        self.__logger = logger
        self.__kite = auth.get_kite()


    def get_positions_all(self) -> List[dict]:
        # NOTE ONLY WORKS FOR BUY POSITION
        """
        return { 975873: {'tradingsymbol': 'ZEEL', 'exchange': 'NSE', 'instrument_token': 975873, 'product': 'CNC',
         'quantity': 0, 'overnight_quantity': 0, 'multiplier': 1, 'average_price': 0, 'close_price': 0,
         'last_price': 220.65, 'value': 0.25, 'pnl': 0.25, 'm2m': 0.25, 'unrealised': 0.25, 'realised': 0, '
         buy_quantity': 5, 'buy_price': 220.25, 'buy_value': 1101.25, 'buy_m2m': 1101.25, 'sell_quantity': 5,
        'sell_price': 220.3, 'sell_value': 1101.5, 'sell_m2m': 1101.5, 'day_buy_quantity': 5,
         'day_buy_price': 220.25, 'day_buy_value': 1101.25, 'day_sell_quantity': 5, 'day_sell_price': 220.3,
         'day_sell_value': 1101.5}}
         """
        return self.__kite.positions()

    def get_position_cnc(self) -> List[OpenPosition]:
        positions = self.__kite.positions()
        return [
            OpenPosition(
                symbol=position['symbol'],
                instrument_token=position['instrument_token'],
                exchange=position['exchange'],
                quantity=position['quantity'],
                average_price=position['average_price'],
            ) for position in positions['net'] if position['product'] == 'CNC'
        ]

    def get_position_mis(self) -> List[OpenPosition]:
        positions = self.__kite.positions()
        return [
            OpenPosition(
                symbol=position['symbol'],
                instrument_token=position['instrument_token'],
                exchange=position['exchange'],
                quantity=position['quantity'],
                average_price=position['average_price'],
            ) for position in positions['net'] if position['product'] == 'MIS'
        ]

    def get_positions(self) -> List[OpenPosition]:
        positions = self.__kite.positions()
        return [
            OpenPosition(
                symbol=position['symbol'],
                instrument_token=position['instrument_token'],
                exchange=position['exchange'],
                quantity=position['quantity'],
                average_price=position['average_price'],
            ) for position in positions['net']
        ]

    def get_holdings(self) -> List[OpenPosition]:
        holdings = self.__kite.holdings()
        return [
            OpenPosition(
                symbol=position['symbol'],
                instrument_token=position['instrument_token'],
                exchange=position['exchange'],
                quantity=position['t1_quantity'] if position['t1_quantity'] > 0 else position['quantity'],
                average_price=position['average_price'],
            ) for position in holdings['net'] if position['product'] == 'CNC'
        ]

    def get_position_holding_all(self):
        positions = self.get_positions()
        holdings = self.get_holdings()
