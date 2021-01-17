import click
from lib import dependencies
from lib import log
from flask import Blueprint
from services.strategy import MacdStrategy
from typing import List

blueprint = Blueprint('strategy', __name__)


@blueprint.cli.command("macd")
@click.argument('tokens', nargs=-1)
def macd(tokens: List[str]):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    macd_strategy = injector.get(MacdStrategy)
    logger.info(f"macd strategy starting for token {tokens}.")
    macd_strategy.run([int(token) for token in tokens])
    logger.info("macd strategy stopped.")


