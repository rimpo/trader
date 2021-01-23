import click
from lib import dependencies
from lib import log
from datetime import datetime, timedelta
from pytimeparse import parse
from flask import Blueprint
from lib.time import india
from services.historical_data.historical_data import HistoricalDataService
import time
from typing import List
from lib.telegram_bot import TelegramBot
from lib.time import TimeRange, IndiaTimeService, NSEExchangeTime, TimeSleepWait, DummyExchangeTime, \
    DummySleepWait, GermanyTimeService, DummyTimeService, DummySleepWait

blueprint = Blueprint('historical-data', __name__)

@blueprint.cli.command("test-time")
@click.option('--interval', default=5, type=int)
@click.argument('tokens', nargs=-1)
def test(tokens: List[str], interval: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    from_date = india.localize(datetime(2021, 1, 22, 9, 10, 0))
    # time_range = TimeRange(interval=interval, time_service=IndiaTimeService(), exchange_time=NSEExchangeTime, time_wait=TimeSleepWait(seconds=15))
    time_range = TimeRange(
        interval=interval,
        time_service=DummyTimeService(from_date, 1),
        exchange_time=NSEExchangeTime(),
        time_wait=DummySleepWait()
    )
    for t in time_range.get_next():
        curr_time = datetime.utcnow().astimezone(india)
        logger.info(f"curr:{curr_time} got:{t} ")



@blueprint.cli.command("test1")
@click.option('--interval', default=15, type=int)
@click.argument('tokens', nargs=-1)
def test(tokens: List[str], interval: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    historical_data_service = injector.get(HistoricalDataService)

    to_date = india.localize(datetime.utcnow())
    now_utc = india.localize(datetime.utcnow())

    from_date = india.localize(datetime(now_utc.year, now_utc.month, 20, 9, 15, 0))
    logger.info(f"from_date:{from_date} to_date:{to_date}")
    for token in tokens:
        historical_data_service.download_and_save(token, interval, from_date, to_date)
    logger.info("done.")


@blueprint.cli.command("test")
@click.option('--interval', default=15, type=int)
@click.argument('tokens', nargs=-1)
def test(tokens: List[str], interval: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    historical_data_service = injector.get(HistoricalDataService)

    to_date = india.localize(datetime.utcnow())
    # from_date = to_date - timedelta(days=30)
    now_utc = india.localize(datetime.utcnow())
    from_date = india.localize(datetime(now_utc.year, now_utc.month, 22, 15, 15, 0))
    logger.info(f"from_date:{from_date} to_date:{to_date}")

    from_date = from_date.replace(day=20)

    data = historical_data_service.get_candle(tokens[0], interval, from_date)
    logger.info(f"candle:{data}")

    data = historical_data_service.get_candles(tokens[0], interval, 5, from_date)
    logger.info(data)


@blueprint.cli.command("sync")
@click.option('--interval', default=15)
@click.option('--sleep-seconds', default=10)
@click.option('--since', default="5d")
@click.argument('tokens', nargs=-1)
def sync(tokens: List[str], interval: int, sleep_seconds: int, since: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    historical_data_service = injector.get(HistoricalDataService)
    telegram_bot = injector.get(TelegramBot)

    to_date = datetime.utcnow().astimezone(india) - timedelta(minutes=interval)
    from_date = to_date - timedelta(seconds=parse(since))
    for token in tokens:
        historical_data_service.download_and_save(token, interval, from_date, to_date)

    # NOTE: THIS ONLY WORKS FOR INTERVAL WITHIN ONE HOUR
    try:
        while True:
            curr_time = datetime.utcnow().astimezone(india)
            curr_time = curr_time.replace(second=0, microsecond=0)
            if curr_time.minute % interval == 0:
                for_date = curr_time - timedelta(minutes=interval + 1)  # Note: 1 minute will not work
                for token in tokens:
                    logger.info(f"token:{token}  wait for curr_time:{curr_time} for_date:{for_date}")
                    historical_data_service.wait_download_and_save(token, for_date, interval, sleep_seconds)
            time.sleep(10)
    except Exception as e:
        logger.exception(f"failed sync {e}")
        telegram_bot.send("historical data sync failed !!")






