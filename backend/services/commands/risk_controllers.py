import click
from lib import dependencies
from lib import log
from flask import Blueprint
from services.strategy import MacdStrategy
from lib.mongo_db import db
import time
from services.order import PositionService
from services.instruments import InstrumentService
from lib.config import env
from lib.telegram_bot import TelegramBot

blueprint = Blueprint('risk', __name__)


@blueprint.cli.command("simple")
@click.argument('tokens', nargs=-1)
def macd(tokens: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    position_service = injector.get(PositionService)
    instrument_service = injector.get(InstrumentService)
    telegram_bot = injector.get(TelegramBot)

    loss_percent_allowed = 1.5
    exit_percent_profit = [1.1, 1.6, 2.1]
    tokens = [int(token) for token in tokens]

    positions = {}

    while True:
        # fetch positions
        prices = instrument_service.get_ltp(tokens)
        positions = position_service.get_open_position()
        signal = db["signals"].find({"processed": False}).limit(1)
        if signal:
            token = signal['instrument_token']
            qty = positions[token ]
            if qty > 0 and signal["signal"] == "SELL":
                # close all position
                telegram_bot.send(f"{token} SELL all")
                pass
            elif qty > 0 and signal["signal"] == "BUY":
                # do nothing. we are in the right
                pass
            elif qty <= 0 and signal["signal"] == "BUY":
                # buy stock
                telegram_bot.send(f"{token} BUY 100 {prices[token]}")
                pass

        for token in tokens:
            pass
                # if loss percent hit
                    # close all position
                # if profit level 1
                    # close 50 %
                # if profit level 2
                    # close 50 %
        time.sleep(15)


