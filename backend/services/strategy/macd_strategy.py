from lib import log
from services.candles import CandleService

import pandas as pd
import numpy as np
import talib
from talib.abstract import EMA, SMA
from injector import inject

from lib.algos import cross

class MacdIndicator:
    def __init__(self, logger: log.Logger, fast_ema_length: int, slow_ema_length: int, signal_length: int):
        self.__logger = logger
        self.__fast_ema_length = fast_ema_length
        self.__slow_ema_length = slow_ema_length
        self.__signal_length = signal_length

    def calculate(self, candles) -> (bool, bool):
        df = pd.DataFrame.from_dict(candles)

        df['fast_ema'] = EMA(df['close'].values, timeperiod=self.__fast_ema_length)
        df['slow_ema'] = EMA(df['close'].values, timeperiod=self.__slow_ema_length)
        df['macd'] = df['fast_ema'] - df['slow_ema']
        df['signal'] = SMA(df['macd'].values, timeperiod=self.__signal_length)

        macd = df['macd'].iloc[-1]
        signal = df['signal'].iloc[-1]

        macd_is_above = macd >= signal
        macd_is_below = macd < signal

        previous_macd = df['macd'].shift(1).iloc[-1]
        previous_signal = df['signal'].shift(1).iloc[-1]
        crossing = cross(previous_macd, previous_signal, macd, signal)
        return crossing, macd_is_above

class MacdStrategy:
    @inject
    def __init__(self, logger: log.Logger, token: int, candle_service: CandleService):
        self.__logger = logger
        self.__token = token
        self.__candle_service = candle_service
        self.__macd_indicator = MacdIndicator(logger, fast_ema_length=12, slow_ema_length=26, signal_length=9)

    def process_candles(self):
        candles = self.__candle_service.get_candles(self.__token, "15minute", 50)
        self.__macd_indicator.calculate(candles)


