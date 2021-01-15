from typing import List
from kiteconnect import KiteTicker
from lib.config import env
from lib.mongo_db import db
from mongoengine import connect
from lib import dependencies
from lib import log
import time
from pytz import timezone
from services.auth import auth
from collections import defaultdict

india = timezone('Asia/Kolkata')


def run_app():
    connect(env.DB_NAME, host=env.DB_HOST, port=int(env.DB_PORT))

    log.initialize_root_logger()

    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    auth_service = injector.get(auth.AuthService)

    logger.info("starting ticker service")

    candles = defaultdict(dict)

    def create_candle(tick):
        candles[tick['instrument_token']] = {
            "instrument_token": tick['instrument_token'],
            "open": tick["last_price"],
            "close": tick["last_price"],
            "high": tick["last_price"],
            "low": tick["last_price"],
            "volume": tick["last_quantity"],
            "date": tick["last_trade_time"],
        }

    def update_candle(tick):
        candle = candles[tick['instrument_token']]
        if candle["date"].minute != tick["last_trade_time"].minute and tick["last_trade_time"].minute % 5 == 0:
            # r.db(env.DB_NAME).table('tick_1m').insert('')
            logger.info(candle)
            # send candle
            create_candle(tick)
            # reset candle
        if candle["high"] < tick["last_price"]:
            candle["high"] = tick["last_price"]
        if candle["low"] > tick["last_price"]:
            candle["low"] = tick["last_price"]
        candle["close"] = tick["last_price"]
        candle["date"] = tick["last_trade_time"].replace(second=0, microsecond=0)
        candle["volume"] = tick["last_quantity"] + candle["volume"]

    def process_ticks(ticks):
        for tick in ticks:
            tick['last_trade_time'] = tick['last_trade_time'].astimezone(india)
            tick['timestamp'] = tick['timestamp'].astimezone(india)
            if tick['instrument_token'] in candles:
                update_candle(tick)
            else:
                create_candle(tick)

    def on_ticks(ws, ticks):
        pass

    def on_connect(ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        ws.subscribe([975873,])
        # Set RELIANCE to tick in `full` mode.
        ws.set_mode(ws.MODE_FULL, [975873,])

    def on_close(ws, code, reason):
        # On connection close stop the main loop
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()

    logger.info(f"token:{auth_service.get_access_token()}")

    kws = KiteTicker(api_key=env.KITE_API_KEY, access_token=auth_service.get_access_token())


    # Assign the callbacks.
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close

    # Infinite loop on the main thread. Nothing after this will run.
    # You have to use the pre-defined callbacks to manage subscriptions.
    kws.connect(threaded=True)

    logger.info("start processing!!")
    while True:
        def on_ticks(ws, ticks):
            process_ticks(ticks)
        kws.on_ticks = on_ticks
        time.sleep(0.1)
