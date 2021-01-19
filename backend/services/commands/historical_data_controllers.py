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

blueprint = Blueprint('historical-data', __name__)


@blueprint.cli.command("test")
@click.option('--interval', default=15, type=int)
@click.argument('tokens', nargs=-1)
def test(token: List[str], interval: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    historical_data_service = injector.get(HistoricalDataService)

    now_utc = datetime.utcnow()
    from_date = india.localize(datetime(now_utc.year, now_utc.month, now_utc.day, 13, 0, 0))
    to_date = from_date + timedelta(minutes=interval)

    logger.info(f"from_date:{from_date} to_date:{to_date}")

    historical_data_service.download_and_save(token, interval, from_date, to_date)
    logger.info("done.")

    data = historical_data_service.get_candle(int(token), interval, from_date)
    logger.info(data)


@blueprint.cli.command("sync")
@click.option('--interval', default=15)
@click.option('--sleep-seconds', default=10)
@click.option('--since', default="3d")
@click.argument('tokens', nargs=-1)
def sync(tokens: List[str], interval: int, sleep_seconds: int, since: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    historical_data_service = injector.get(HistoricalDataService)

    # Download historical data from now to some defined time in the past
    to_date = datetime.utcnow().astimezone(india)
    from_date = to_date - timedelta(seconds=parse(since))
    for token in tokens:
        historical_data_service.download_and_save(token, interval, from_date, to_date)

    # NOTE: THIS ONLY WORKS FOR INTERVAL WITHIN ONE HOUR
    try:
        while True:
            curr_time = datetime.utcnow().astimezone(india)
            if curr_time.minute % interval == 0:
                logger.info(f"token:{token} from_date:{from_date} to_date:{to_date}")
                for token in tokens:
                    historical_data_service.wait_download_and_save(token, curr_time, interval, sleep_seconds)
            else:
                logger.info(f"{curr_time.minute} waiting for the time")
                time.sleep(5)
                continue
    except Exception as e:
        logger.error(f"failed sync {e}")
        pass






