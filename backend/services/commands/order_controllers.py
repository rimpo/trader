from .controllers import blueprint
import click
from lib import dependencies
from lib import log
from services.external.kite.order import MarketOrderService
from services.order.position import PositionService
from services.order import HoldingService

from flask import Blueprint

blueprint = Blueprint('order', __name__)

@blueprint.cli.command("place")
@click.option('--s', required=True, type=str)
@click.option('--bs', required=True, type=str)
@click.option('--q', required=True, type=int)
def order(s: str, bs: str, q: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    order_service = injector.get(MarketOrderService)

    if bs == "B":
        order_service.buy_market_order_cnc(s, q)
    else:
        order_service.sell_market_order_cnc(s, q)


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


