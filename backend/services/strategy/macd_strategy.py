from lib import log
from services.historical_data.historical_data import HistoricalDataService

import pandas as pd
from talib.abstract import EMA, SMA, MACDEXT
from injector import inject

from lib.algos import cross
from datetime import datetime, timedelta
from lib.time import india
import time
import pymongo
from lib.mongo_db import  db
from typing import List
import pytz
from services.strategy.signal import SignalService

class MacdIndicator:
    @inject
    def __init__(self, logger: log.Logger, fast_ema_length: int, slow_ema_length: int, signal_length: int):
        self.__logger = logger
        self.__fast_ema_length = fast_ema_length
        self.__slow_ema_length = slow_ema_length
        self.__signal_length = signal_length

    def calculate(self, candles) -> (bool, bool):

        df = pd.DataFrame.from_dict(candles)

        df['macd'], df['signal'], _ = MACDEXT(
            df['close'],
            fastperiod=self.__fast_ema_length,
            fastmatype=1,
            slowperiod=self.__slow_ema_length,
            slowmatype=1,
            signalperiod=self.__signal_length,
            signalmatype=0
        )

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
    def __init__(self, logger: log.Logger, historical_data_service: HistoricalDataService, signal_service: SignalService):
        self.__logger = logger
        self.__historical_data_service = historical_data_service
        self.__macd_indicator = MacdIndicator(logger, fast_ema_length=12, slow_ema_length=26, signal_length=5)
        self.__signal_service = signal_service
        self.__no_of_candles = 50

    def run(self, tokens: List[str], interval: int):
        now_utc = datetime.utcnow()
        from_date = india.localize(datetime(now_utc.year, now_utc.month, now_utc.day, 9, 15, 0))


        while True:
            # JUMPING to the right time
            now_utc = datetime.utcnow().astimezone(india)
            if from_date + timedelta(minutes=interval) < now_utc:
                # self.__logger.debug(f"ignore {from_date}")
                from_date += timedelta(minutes=interval)
                continue

            for token in tokens:
                # COMPLICADO - waiting for data to arrive
                while True:
                    data = self.__historical_data_service.get_for_date(token, interval, from_date)
                    if data is not None:
                        self.__logger.debug(f"data {token} {interval}min {from_date} {data}. Yay !!")
                        break
                    time.sleep(15)
                    self.__logger.debug(f"token:{token} data not found for {from_date} :(")
                    continue

                candles = self.__historical_data_service.get_candles(token, interval, self.__no_of_candles)
                candles.reverse()
                crossing, macd_is_above = self.__macd_indicator.calculate(candles)
                if crossing:
                    if macd_is_above:
                        self.__signal_service.save_buy_signal(token, datetime.utcnow())
                        self.__logger.debug(f"buy signal for {token}!!")
                    else:
                        self.__signal_service.save_sell_signal(token, datetime.utcnow())
                        self.__logger.debug(f"sell signal for {token}!!")
            from_date += timedelta(minutes=interval)


