from talib import RSI, WMA
import pandas as pd
from talib.abstract import EMA, SMA
import numpy as np
_
class HilegaMilegaIndicator:
    def __init__(self):
        pass

    def calculate(self, candles):
        df = pd.DataFrame.from_dict(candles)
        df['rsi'] = RSI(df['close'].values(), timeperiod=9)
        df['wma'] = WMA(df['rsi'].values(), timeperiod=21)
        df['ema'] = EMA(df['rsi'].values(), timeperiod=3)
        vwap = np.cumsum((df['volume'].values() * (df['high'].values() + df['low'].values() / 2)) / np.cumsum(df['volume'].values()))

        ema = df['rsi'].iloc[-1]
        wma = df['wma'].iloc[-1]
        rsi = df['ema'].iloc[-1]


