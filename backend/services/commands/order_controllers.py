from .controllers import blueprint
import click
from lib import dependencies
from lib import log
from services.external.kite.order import OrderService

from flask import Blueprint

blueprint = Blueprint('order', __name__)

@blueprint.cli.command("place")
@click.option('--s', required=True, type=str)
@click.option('--bs', required=True, type=str)
@click.option('--q', required=True, type=int)
def order(s: str, bs: str, q: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    order_service = injector.get(OrderService)

    if bs == "B":
        order_service.buy_market_order_cnc(s, q)
    else:
        order_service.sell_market_order_cnc(s, q)
