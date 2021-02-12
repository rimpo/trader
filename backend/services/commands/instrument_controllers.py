from .controllers import blueprint
import click
from lib import dependencies
from lib.config import env
from lib import log
from services.instruments import InstrumentService
from services.auth import AuthService
from typing import List

from flask import Blueprint

blueprint = Blueprint('instrument', __name__)

@blueprint.cli.command("ltp")
@click.argument('symbols', nargs=-1)
def ltp(symbols: List[str]):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    instrument_service = injector.get(InstrumentService)
    prices = instrument_service.get_symbol_ltp("NFO", [ symbol for symbol in symbols])
    logger.info(f"prices: {prices}")
    # prices: {'NSE:468HR22-SG': {'instrument_token': 5541889, 'last_price': 0}, 'NSE:ZEEL': {'instrument_token': 975873, 'last_price': 224.9}}


@blueprint.cli.command("download")
def create_instrument():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    instrument_service = injector.get(InstrumentService)
    instrument_service.create_instruments()
    logger.info("NSE instrument download complete.")


@blueprint.cli.command("auth-renew")
@click.argument('tokens', nargs=-1)
def auth_renew(tokens: List[str]):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    auth_service = injector.get(AuthService)
    auth_service.renew_access_token()
    instrument_service = injector.get(InstrumentService)
    prices = instrument_service.get_ltp([int(token) for token in tokens])
    logger.info(f"prices: {prices}")
