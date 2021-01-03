
from dataclasses import dataclass
from datetime import datetime

"""
Sample tick packet
[{'tradable': True, 'mode': 'full', 'instrument_token': 69121, 'last_price': 493.85, 'last_quantity': 24, 'average_pric
e': 469.78, 'volume': 5299040, 'buy_quantity': 553795, 'sell_quantity': 202952, 'ohlc': {'open': 454.9, 'high': 497.7, 'low': 448.2, 'clo
se': 435.9}, 'change': 13.294333562743759, 'last_trade_time': datetime.datetime(2020, 12, 31, 10, 38, 38), 'oi': 0, 'oi_day_high': 0, 'oi
_day_low': 0, 'timestamp': datetime.datetime(2020, 12, 31, 10, 38, 39), 'depth': {'buy': [{'quantity': 75, 'price': 493.75, 'orders': 1},
 {'quantity': 2, 'price': 493.65, 'orders': 2}, {'quantity': 12, 'price': 493.5, 'orders': 2}, {'quantity': 32, 'price': 493.45, 'orders'
: 1}, {'quantity': 200, 'price': 493.4, 'orders': 1}], 'sell': [{'quantity': 342, 'price': 493.85, 'orders': 1}, {'quantity': 536, 'price
': 493.9, 'orders': 1}, {'quantity': 4, 'price': 493.95, 'orders': 3}, {'quantity': 75, 'price': 494.0, 'orders': 5}, {'quantity': 37, 'p
rice': 494.05, 'orders': 2}]}}]
"""

@dataclass(frozen=False)
class Tick:
    tradable: bool
    mode: str
    instrument_token: int
    last_price: float
    last_quantity: float
    average_price: float
    volume: float
    last_trade_time: datetime
    timestamp: datetime

    def __init__(self, tick):
        self.tradable = tick['tradable']
        self.mode = tick['mode']
        self.instrument_token = tick['instrument_token']
        self.last_price = tick['last_price']
        self.last_quantity = tick['last_quantity']
        self.average_price = tick['average_price']
        self.volume = tick['volume']
        self.last_trade_time = tick['last_trade_time']
        self.timestamp = tick['timestamp']

