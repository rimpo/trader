import json
import logging
from datetime import datetime
from dataclasses import dataclass
from kiteconnect import KiteTicker
#from kiteconnect import KiteConnect
from config import API_KEY, ACCESS_TOKEN, INSTRUMENT_FILE
from lib import VWAP
from lib import FormCandle, sample
from lib import Tick
import numpy as np
import talib
import time
from talib.abstract import EMA, STOCHRSI


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('generate_instruments')

#ITC 424961
subscribed_tokens = [424961, ]

form_candle = FormCandle()
# vwap = VWAP()


def on_test_sample(candles):
    close50 = []
    for candle in candles:
        print(candle)
        close50.append(float(candle['close']))
        if len(close50) > 50:
            close50.pop(0)
        np_ema20 = EMA({'close': np.array(close50)}, timeperiod=20, price='close')
        np_ema50 = EMA({'close': np.array(close50)}, timeperiod=50, price='close')
        ema20 = np_ema20[-1]
        ema50 = np_ema50[-1]
        diff = ema20 - ema50
        print(f"{candle['date']}, {diff}, {ema20}, {ema50}")
        # print(f'EMA20:{ema20} EMA50:{ema50} diff={ema20-ema50}')

on_test_sample(sample)

exit()




def on_ticks(ws, ticks):
    # logging.debug("Ticks: {}".format(ticks))
    # Callback to receive ticks.
    for tick in ticks:
        t = Tick(tick)
        candle = form_candle.process(t)
        if candle is not None:
            # calculate vwap
            # calculate ema 20 and 50
            # if 20 and 50 create increasing gap - generate signal buy or sell
            vwap.calc_tick(tick)
            pass



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


kws = KiteTicker(API_KEY, ACCESS_TOKEN)
# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
