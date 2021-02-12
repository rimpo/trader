from .controllers import blueprint
import click
from lib import dependencies
from lib import log
from services.external.kite import LTPService
from services.order.order import MISMarketOrderService
from services.order.position import PositionService
from services.order import HoldingService
from services.instruments import InstrumentService

from flask import Blueprint

blueprint = Blueprint('order', __name__)

import signal
import time

class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


@blueprint.cli.command("place")
@click.option('--exchange', required=True, type=str)
@click.option('--symbol', required=True, type=str)
@click.option('--qty', required=True, type=int)
@click.option('--maxloss', required=True, type=float)
def order(exchange: str, symbol: str, qty: int, maxloss: float):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    order_service = injector.get(MISMarketOrderService)
    instrument_service = injector.get(InstrumentService)
    killer = GracefulKiller()

    maxloss = -1 * maxloss

    # order_service.buy(exchange, symbol, qty)
    prices = instrument_service.get_symbol_ltp(exchange, [symbol, ])
    approx_traded_price = prices[f"{exchange}:{symbol}"]["last_price"]
    total_value = approx_traded_price * qty
    logger.info(f"exchange:{exchange} symbol:{symbol} approx_traded_price:{approx_traded_price}")

    while not killer.kill_now:
        prices = instrument_service.get_symbol_ltp(exchange, [symbol, ])
        ltp = prices[f"{exchange}:{symbol}"]["last_price"]
        profit = ltp * qty - total_value
        logger.info(f"current profit: {profit} ltp:{ltp} bought_price:{approx_traded_price}")
        if maxloss > ltp * qty - total_value:
            # order_service.sell(exchange, symbol, qty)
            logger.info(f"exiting with loss: {profit}  bought_price:{approx_traded_price} :(")
            quit(0)
            break
        time.sleep(0.5)
    # order_service.sell(exchange, symbol, qty)
    prices = instrument_service.get_symbol_ltp(exchange, [symbol, ])
    ltp = prices[f"{exchange}:{symbol}"]["last_price"]
    profit = ltp * qty - total_value
    logger.info(f"exit with profit: {profit} ltp:{ltp} bought_price:{approx_traded_price}")


@blueprint.cli.command("open-position")
def open_position():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    position_service = injector.get(PositionService)

    positions = position_service.get_open_position()
    logger.info(positions)

@blueprint.cli.command("open-holding")
def holding_test():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    holding_service = injector.get(HoldingService)
    holdings = holding_service.get_open_holding()
    logger.info(f"holdings:{holdings}")


