from lib import log
from services.candles import CandleService

import pandas as pd
import numpy as np
import talib
from talib.abstract import EMA, SMA


class MacdStrategy:
    def __init__(self, logger: log.Logger, token: int, candle_service: CandleService):
        self.__logger = logger
        self.__token = token
        self.__candle_service = candle_service

    def process_candle(self):
        fast_ema_length = 12
        slow_ema_length = 26
        signal_length = 9

        candles = self.__candle_service.get_candle(self.__token, "15minute", slow_ema_length)

        df = pd.Dataframe.from_dict(candles)

        df['fast_ema'] = EMA(df['close'].values, timeperiod=fast_ema_length)
        df['slow_ema'] = EMA(df['close'].values, timeperiod=slow_ema_length)
        df['signal'] = df['fast_ema'] - df['slow_ema']
        df['macd'] = SMA(df['signal'].values, timeperiod=signal_length)
