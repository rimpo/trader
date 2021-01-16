import click
from .controllers import blueprint
from lib import dependencies
from lib import log
from kiteconnect import KiteConnect
from services.auth import auth
from pytz import timezone
from datetime import datetime, timedelta
from pytimeparse import parse
from lib.mongo_db import db
from flask import Blueprint
from lib.time import india

blueprint = Blueprint('historical-data', __name__)



@blueprint.cli.command("sync")
@click.option('--token', required=True, type=str)
@click.option('--period', default="15minute")
@click.option('--sleep-seconds', default=15)
def sync_candle(token, period: str, sleep_seconds: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)

    now_utc = datetime.utcnow()
    from_date = india.localize(datetime(now_utc.year, now_utc.month, now_utc.day, 9, 14, 0))
    to_date = from_date + timedelta(minutes=15)

    fmt = '%Y-%m-%d %H:%M:%S'

    expected_dt = india.localize(datetime(now_utc.year, now_utc.month, now_utc.day, 9, 15, 0))

    while True:
        logger.info(f"{token} from:{from_date} to:{to_date}, period:{period} waiting")
        results = kite.historical_data(
            int(token),
            from_date.strftime(fmt),
            to_date.strftime(fmt),
            interval=period,
            continuous=False, oi=True
        )
        if results > 0:
            from_date += timedelta(minutes=15)
            to_date += timedelta(minutes=15)

        logger.info(f"result:{results}")


@blueprint.cli.command("download-candles")
@click.option('--token', required=True, type=str)
@click.option('--period', default="5minute")
@click.option('--since', default="30d")
def download_candles(token: str, period: str, since: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    kite = injector.get(KiteConnect)
    _ = injector.get(auth.AuthService)
    india = timezone('Asia/Kolkata')
    now_utc = datetime.utcnow()
    to_date = now_utc.astimezone(india)
    from_date = to_date - timedelta(seconds=parse(since))

    logger.info(f"{token} from:{from_date} to:{to_date}, period:{period}")

    # to_date = india.localize(datetime(2020, 1, 11, 15, 35, 0))
    # from_date = india.localize(datetime(2020, 1, 1, 9, 15, 0))
    fmt = '%Y-%m-%d %H:%M:%S'

    results = kite.historical_data(
        int(token),
        from_date.strftime(fmt),
        to_date.strftime(fmt),
        interval=period,
        continuous=False, oi=True
    )
    if len(results) > 0:
        db[f"ohlc_{token}_{period}"].insert_many(results)
