import click
from lib import dependencies
from lib import log
from flask import Blueprint
from services.strategy import MacdStrategy
from lib.mongo_db import db
import time
from services.order import PositionService
from services.instruments import InstrumentService
from services.strategy.signal import SignalService
from lib.config import env
from lib.telegram_bot import TelegramBot

blueprint = Blueprint('risk', __name__)


def is_ltp_in_loss(ltp: float, avg_price: float, percent: float) -> bool:
    # stop loss condition
    return (avg_price - (avg_price * percent/100.0)) >= ltp


def is_ltp_in_profit(ltp: float, avg_price: float, percent: float) -> bool:
    return ltp > (avg_price + (avg_price*percent)/100.0)


def get_qty_to_close(qty, max_buy_quantity):
    if qty == max_buy_quantity:
        return qty/4
    elif qty == 3*max_buy_quantity/4:
        return qty/4
    else:
        return qty


@blueprint.cli.command("simple")
@click.argument('tokens', nargs=-1)
def simple(tokens: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    position_service = injector.get(PositionService)
    instrument_service = injector.get(InstrumentService)
    signal_service = injector.get(SignalService)
    telegram_bot = injector.get(TelegramBot)

    tokens = [int(token) for token in tokens]
    # Note: quantity should be divisible by 4
    max_buy_quantity =  12
    flat_stop_loss_percent = 1.5

    while True:
        positions = position_service.get_open_position()
        signal = signal_service.get_unprocessed_signal(tokens)
        prices = instrument_service.get_ltp(tokens)
        if signal:
            # TAKE POSITION
            position = positions[signal.instrument_token]

            if position['quantity'] > 0:
                if signal.is_buy_signal():
                    # do nothing we are already long
                    pass
                else:
                    # close long position
                    telegram_bot.send(f"{signal.instrument_token} SELL all")
            elif position['quantity'] < 0:
                if signal.is_buy_signal():
                    # close short position
                    # TODO: sake of simplicity not going long
                    telegram_bot.send(f"{signal.instrument_token} BUY 100 {prices[signal.instrument_token]}")
                else:
                    # do nothing we are already short
                    pass
            else:
                if signal.is_buy_signal():
                    telegram_bot.send(f"{signal.instrument_token} BUY long")
                else:
                    # TODO: short only when time is less 12:00pm and price is below 50 EMA
                    # TODO: sake of simplicity not going long
                    telegram_bot.send(f"{signal.instrument_token} SELL short")
            signal_service.set_signal_processed(signal.id)
        else:
            # MANAGE RISK - BY REDUCING POSITION ON PROFIT
            for token in tokens:
                ltp = prices[token]
                avg_price = position['average_price']
                qty = position['quantity']
                if is_ltp_in_loss(ltp, avg_price, flat_stop_loss_percent):
                    # TODO call sell all
                    pass
                if is_ltp_in_profit(ltp, avg_price, 1.0):
                    qty_to_close = get_qty_to_close(qty, max_buy_quantity)
                    # TODO: call sell
                if is_ltp_in_profit(ltp, avg_price, 1.5):
                    qty_to_close = get_qty_to_close(qty, max_buy_quantity)
                    # TODO: call sell

        time.sleep(15)


