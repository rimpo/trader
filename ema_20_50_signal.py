import json
import logging
import datetime
from dataclasses import dataclass
from kiteconnect import KiteTicker
#from kiteconnect import KiteConnect
from config import API_KEY, ACCESS_TOKEN, INSTRUMENT_FILE
from lib import VWAP
from lib import FormCandle
from lib import Tick
import numpy as np
import talib
from talib.abstract import EMA
import telegram

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ema')

# Load instruments
def load_instrument(exchange: str) -> dict:
    with open(INSTRUMENT_FILE) as json_file:
        instruments = json.load(json_file)
        return instruments

instruments = load_instrument("NSE")
instruments_lookup = {}
for instrument in instruments:
    instruments_lookup[instrument["tradingsymbol"]] = instrument



bot = telegram.Bot(token='1425679142:AAE9atCywGO4JApJ9Grzt3j-AaLbSnvUxOI')

subscribed_symbols = ["TCS", "L&TFH", "CHEMCON"]

subscribed_tokens = []
for symbol in subscribed_symbols:
    subscribed_tokens.append(instruments_lookup[symbol]["instrument_token"])

def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def strictly_decreasing(L):
    return all(x>y for x, y in zip(L, L[1:]))

class TokenInfo:

    NO_SIGNAL = 0
    BUY_SIGNAL = 1
    SELL_SIGNAL = 2

    MAX_DIFF_CHECK = 3

    def __init__(self, token, symbol):
        self.close50 = []
        self.diffs = []
        self.current_signal = self.NO_SIGNAL
        self.token = token
        self.symbol = symbol
        self.form_candle = FormCandle()




    def process(self, tick: Tick):
        # populate with the first tick as close price
        if len(self.close50) == 0:
            for _ in range(49):
                self.close50.append(tick.last_price)

        candle = self.form_candle.process(tick)

        if candle is None:
            return

        self.close50.append(float(candle.close_price))

        #keep the max size as 50
        if len(self.close50) > 50:
            self.close50.pop(0)

        # calculate EMA 20 and 50
        inputs = {'close': np.array(self.close50)}
        np_ema20 = EMA(inputs, timeperiod=20, price='close')
        np_ema50 = EMA(inputs, timeperiod=50, price='close')
        ema20 = np_ema20[-1]
        ema50 = np_ema50[-1]

        diff = ema20 - ema50
        # getting rid of fractions
        clean_diff = int(diff * 1000)

        self.diffs.append(clean_diff)

        # not enough diff no need to check diffs
        if len(self.diffs) < self.MAX_DIFF_CHECK:
            return

        # remove the access diffs
        if len(self.diffs) > self.MAX_DIFF_CHECK:
            self.diffs.pop(0)

        # ignoring the initial signal until a reversal happens
        if self.current_signal == self.NO_SIGNAL:
            # checking reversal
            if self.diffs[-1] < 0.0 and self.diffs[-2] > 0.0:
                # setting signal opposite of the latest direction since we have check current_signal != BUY_SIGNAL
                self.current_signal = self.BUY_SIGNAL
            if self.diffs[-1] > 0.0 and self.diffs[-2] < 0.0:
                # setting signal opposite of the latest direction since we have check current_signal != SELL_SIGNAL
                self.current_signal = self.SELL_SIGNAL
            else:
                # still waiting for the first reversal
                logger.info(f"waiting first reversal for {self.symbol}")
                return

        if self.current_signal != self.SELL_SIGNAL and self.diffs[-1] < 0.0 and strictly_decreasing(self.diffs):
            # send sell signal
            message = f"""{self.symbol} Sell Signal. trade_price: {tick.last_price} trade_time:{tick.last_trade_time} diffs:{self.diffs} candle:{candle} """
            logger.info(message)
            bot.send_message(chat_id=-462939300, text=message)
            self.current_signal = self.SELL_SIGNAL
        if self.current_signal != self.BUY_SIGNAL and self.diffs[-1] < 0.0 and strictly_increasing(self.diffs):
            # send buy signal
            message = f"""{self.symbol} Buy Signal.  trade_price: {tick.last_price} trade_time:{tick.last_trade_time} diffs:{self.diffs} candle:{candle}"""
            logger.info(message)
            bot.send_message(chat_id=-462939300, text=message)
            self.current_signal = self.BUY_SIGNAL

token_details = {}
for symbol in subscribed_symbols:
    token = instruments_lookup[symbol]["instrument_token"]
    token_details[token] = TokenInfo(token, symbol)


def on_ticks(ws, ticks):
    # logging.debug("Ticks: {}".format(ticks))
    for tick in ticks:
        t = Tick(tick)
        token_details[tick['instrument_token']].process(t)


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe(subscribed_tokens)

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, subscribed_tokens)
    logger.info(f"token: {subscribed_tokens} subscribed")

def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()
    logger.error("on_close called")

def on_reconnect(ws, attemps_count):
    logger.warning(f"reconnect attempt {attemps_count}")


def test_on_ticks():
    received_ticks = [
        {'tradable': True, 'mode': 'full', 'instrument_token': 69121, 'last_price': 500.75, 'last_quantity': 15,
         'average_price': 519.39, 'volume': 7108449, 'buy_quantity': 240574, 'sell_quantity': 426125,
         'ohlc': {'open': 497.0, 'high': 535.9, 'low': 491.0, 'close': 499.15}, 'change': 3.3256536111389408,
         'last_trade_time': datetime.datetime(2021, 1, 1, 10, 18, 45), 'oi': 0, 'oi_day_high': 0, 'oi_day_low': 0,
         'timestamp': datetime.datetime(2021, 1, 1, 10, 18, 45)},
        {'tradable': True, 'mode': 'full', 'instrument_token': 69121, 'last_price': 515.75, 'last_quantity': 15,
         'average_price': 519.39, 'volume': 7108449, 'buy_quantity': 240574, 'sell_quantity': 426125,
         'ohlc': {'open': 497.0, 'high': 535.9, 'low': 491.0, 'close': 499.15}, 'change': 3.3256536111389408,
         'last_trade_time': datetime.datetime(2021, 1, 1, 10, 18, 45), 'oi': 0, 'oi_day_high': 0, 'oi_day_low': 0,
         'timestamp': datetime.datetime(2021, 1, 1, 10, 18, 45)},
        {'tradable': True, 'mode': 'full', 'instrument_token': 69121, 'last_price': 498.75, 'last_quantity': 15,
         'average_price': 519.39, 'volume': 7108449, 'buy_quantity': 240574, 'sell_quantity': 426125,
         'ohlc': {'open': 497.0, 'high': 535.9, 'low': 491.0, 'close': 450.15}, 'change': 3.3256536111389408,
         'last_trade_time': datetime.datetime(2021, 1, 1, 11, 18, 45), 'oi': 0, 'oi_day_high': 0, 'oi_day_low': 0,
         'timestamp': datetime.datetime(2021, 1, 1, 10, 18, 45)},
    ]
    on_ticks(None, received_ticks)
    exit()

if __name__ == "__main__":
    test_on_ticks()

    kws = KiteTicker(API_KEY, ACCESS_TOKEN)
    # Assign the callbacks.
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close







    # Infinite loop on the main thread. Nothing after this will run.
    # You have to use the pre-defined callbacks to manage subscriptions.
    kws.connect()

