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
from models.ohlc import Ohlc5min

blueprint = Blueprint('dev', __name__)


@blueprint.cli.command("recreate-db")
def recreate_db():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)

    logger.warning(f'{env.DB_USER} permission granted:.')



@blueprint.cli.command("order")
@click.option('--s', required=True, type=str)
@click.option('--bs', required=True, type=str)
@click.option('--q', required=True, type=int)
def order(s: str, bs: str, q: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)

    with get_conn() as conn:
        data = r.db(env.DB_NAME).table('auth').get(1).run(conn)

        if data is None:
            return

        kite = KiteConnect(env.KITE_API_KEY)
        kite.set_access_token(data['access_token'])

        t = None
        if bs == "B":
            t = kite.TRANSACTION_TYPE_BUY
        else:
            t = kite.TRANSACTION_TYPE_SELL

        kite.place_order(kite.VARIETY_REGULAR, kite.EXCHANGE_NSE, s, transaction_type=t,
                         quantity=q, product=kite.PRODUCT_MIS,order_type=kite.ORDER_TYPE_MARKET)

@blueprint.cli.command("position")
def position():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)

    with get_conn() as conn:
        data = r.db(env.DB_NAME).table('auth').get(1).run(conn)

        if data is None:
            return

        kite = KiteConnect(env.KITE_API_KEY)
        kite.set_access_token(data['access_token'])

        p = kite.positions()

        logger.info(p)

        logger.info(kite.orders())

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
    to_date = india.localize(datetime.utcnow())
    from_date = to_date - timedelta(seconds=parse(since))

    logger.info(f"{token} from:{from_date} to:{to_date}, period:{period}")

    # to_date = india.localize(datetime(2020, 1, 11, 15, 35, 0))
    # from_date = india.localize(datetime(2020, 1, 1, 9, 15, 0))
    fmt = '%Y-%m-%d %H:%M:%S'

    results = kite.historical_data(
        int(token),
        from_date.strftime(fmt),
        to_date.strftime(fmt),
        interval="5minute",
        continuous=False, oi=True
    )
    for result in results:
        Ohlc5min(
            token=token,
            date=result['date'],
            open_price=result['open'],
            close_price=result['close'],
            high_price=result['high'],
            low_price=result['low'],
            volume=result['volume'],
        ).save()
    logger.info("save done.")

