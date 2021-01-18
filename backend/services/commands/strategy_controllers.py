import click
from lib import dependencies
from lib import log
from flask import Blueprint
from services.strategy.signal import SignalService
from services.strategy import MacdStrategy
from typing import List

blueprint = Blueprint('strategy', __name__)

@blueprint.cli.command("signal-test")
@click.option('--token', required=True, type=str)
@click.option('--bs', required=True, type=str)
def generate_signal(token: str, bs):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    signal_service = injector.get(SignalService)
    signal_service.save_buy_signal(token)
    logger.info("done {token}")


@blueprint.cli.command("macd")
@click.argument('tokens', nargs=-1)
def macd(tokens: List[str]):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    macd_strategy = injector.get(MacdStrategy)
    logger.info(f"macd strategy starting for token {tokens}.")
    macd_strategy.run(tokens)
    logger.info("macd strategy stopped.")


