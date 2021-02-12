import click
from flask import Blueprint, make_response, request, Response
from lib import dependencies
from lib.config import env
from lib import log
from kiteconnect import KiteConnect
from services.auth import auth
from pytz import timezone
from datetime import datetime, timedelta
from pytimeparse import parse
from lib.mongo_db import db

blueprint = Blueprint('dev', __name__)


@blueprint.cli.command("recreate-db")
def recreate_db():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)

    logger.warning(f'{env.DB_USER} permission granted:.')


@blueprint.cli.command("position")
def position():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    kite = injector.get(KiteConnect)
    _ = injector.get(auth.AuthService)

    p = kite.positions()
    logger.info(p)
    logger.info(kite.orders())



@blueprint.cli.command("macd-strategy")
@click.option('--token', required=True, type=str)
def macd_strategy(token: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)

    from lib.mongo_db import db
    import pandas as pd
    import numpy as np
    import talib
    from talib.abstract import EMA, SMA
    import pymongo
    import time
    from services.strategy import MacdIndicator, Strategy

    india = timezone('Asia/Kolkata')

    period = "15minute"
    token = int(token)
 
    strategy = Strategy(logger)
    macd_indicator = MacdIndicator(logger, fast_ema_length=12, slow_ema_length=26, signal_length=9)

    qty = 100
    offset = 0
    while True:
        candles = db[f"ohlc_{token}_{period}"].find().sort("date", pymongo.ASCENDING).skip(offset).limit(50)

        candles = list(candles)
        if len(candles) != 50:
            break

        crossing, macd_is_buy = macd_indicator.calculate(candles)

        close = candles[-1]['close']
        date = candles[-1]['date']
        date = date + timedelta(hours=5, minutes=30)
        if crossing:
            if macd_is_buy:
                strategy.long_entry(close, qty)
                print(f"{date} BUY {close}")
            else:
                strategy.long_exit(close, qty)
                print(f"{date} SELL {close}")
        offset += 1
    strategy.show()


