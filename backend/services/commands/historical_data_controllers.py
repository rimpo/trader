import click
from lib import dependencies
from lib import log
from datetime import datetime, timedelta
from pytimeparse import parse
from flask import Blueprint
from lib.time import india
from services.historical_data.historical_data import HistoricalDataService
import time

blueprint = Blueprint('historical-data', __name__)


@blueprint.cli.command("test")
@click.option('--token', required=True, type=str)
@click.option('--period', default="15minute")
def test(token, period: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    historical_data_service = injector.get(HistoricalDataService)

    now_utc = datetime.utcnow()
    from_date = india.localize(datetime(now_utc.year, now_utc.month, now_utc.day, 13, 0, 0))
    to_date = from_date + timedelta(minutes=15)

    logger.info(from_date)

    #historical_data_service.download_and_save(token, period, from_date, to_date)
    #logger.info("done.")

    data = historical_data_service.get_for_date(int(token), period, from_date)
    logger.info(data)


@blueprint.cli.command("sync")
@click.option('--token', required=True, type=str)
@click.option('--period', default="15minute")
@click.option('--sleep-seconds', default=10)
@click.option('--since', default="3d")
def sync(token, period: str, sleep_seconds: int, since: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    historical_data_service = injector.get(HistoricalDataService)
    to_date = datetime.utcnow().astimezone(india)
    from_date = to_date - timedelta(seconds=parse(since))

    historical_data_service.download_and_save(token, period, from_date, to_date)

    try:
        while True:
            curr_time = datetime.utcnow().astimezone(india)
            if curr_time.minute not in [0, 15, 30, 45]:
                time.sleep(sleep_seconds)
                continue
            time.sleep(sleep_seconds)

            curr_time = datetime.utcnow().astimezone(india)
            # current time is 9:30:30 then from_date will be 9:13:30
            from_date = curr_time - timedelta(minutes=17)
            historical_data_service.download_and_save(token, period, from_date, curr_time)
            logger.info(f"token:{token} from_date:{from_date} to_date:{to_date}")
    except Exception as e:
        logger.error(f"failed sync {e}")
        pass






