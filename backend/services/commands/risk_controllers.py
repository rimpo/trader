import click
from lib import dependencies
from lib import log
from flask import Blueprint
from services.strategy import MacdStrategy
from lib.mongo_db import db
import time

blueprint = Blueprint('risk', __name__)


@blueprint.cli.command("simple")
@click.argument('tokens', nargs=-1)
def macd(tokens: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)

    loss_percent_allowed = 1.5
    exit_percent_profit = [1.1, 1.6, 2.1]

    # fetch positions

    while True:
        # fetch positions
        signal = db["signals"].find({"processed": False}).limit(1)
        if signal:
            # processing signal
            # fetch signals
            # if signals
            # place order
            # if signal reversed and open position
            # close all position
            pass
        for token in tokens:
            # fetch ltp
            # if open position
                # if loss percent hit
                    # close all position
                # if profit level 1
                    # close 50 %
                # if profit level 2
                    # close 50 %
            pass
        time.sleep(15)


