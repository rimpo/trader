import click
from lib import dependencies
from lib import log
from flask import Blueprint
from services.strategy import MacdStrategy
from lib.mongo_db import db
import time
from services.order import PositionService, MarketOrderServiceCNC, MISMarketOrderService
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
    market_order_service = injector.get(MISMarketOrderService)

    tokens = [int(token) for token in tokens]
    # Note: quantity should be divisible by 4
    max_buy_quantity = 12
    flat_stop_loss_percent = 1.5

    try:
        while True:
            positions = position_service.get_open_position()
            signal = signal_service.get_unprocessed_signal()
            prices = instrument_service.get_ltp(tokens)
            logger.debug("waiting for signal")
            if signal:
                # TAKE POSITION SIGNAL
                position = positions[signal.instrument_token]
                logger.info(f"Got Signal: {signal}!!")
                if position and position['quantity'] != 0:
                    # on valid position
                    if position['quantity'] > 0:
                        if signal.is_buy_signal():
                            # do nothing we are already long
                            pass
                        else:
                            market_order_service.sell(signal.instrument_token, position['quantity'])
                            telegram_bot.send(f"{signal.instrument_token} SELL all")
                    elif position['quantity'] < 0:
                        if signal.is_buy_signal():
                            # close short position
                            # TODO: sake of simplicity not going short
                            telegram_bot.send(f"{signal.instrument_token} BUY 100 {prices[signal.instrument_token]}")
                        else:
                            # do nothing we are already short
                            pass
                else:
                    # on position quantity as 0 or no position
                    if signal.is_buy_signal():
                        market_order_service.buy(signal.instrument_token, max_buy_quantity)
                        telegram_bot.send(f"{signal.instrument_token} BUY long")
                    else:
                        # TODO: short only when time is less 12:00pm and price is below 50 EMA
                        # TODO: sake of simplicity not going short
                        # telegram_bot.send(f"{signal.instrument_token} SELL short")
                        pass
                signal_service.set_signal_processed(signal.id)
            else:
                # MANAGE RISK - BY REDUCING POSITION ON PROFIT

                for token in tokens:
                    if token not in positions:
                        logger.debug("no position is open !")
                        continue
                    position = positions[token]
                    ltp = prices[token]
                    avg_price = position['average_price']
                    qty = position['quantity']
                    logger.debug(f"status: qty:{qty} avg_price:{avg_price} ltp:{ltp}")
                    if qty > 0:
                        if is_ltp_in_loss(ltp, avg_price, flat_stop_loss_percent):
                            # SELL ALL - stop loss hit
                            logger.debug(f"sell: qty:{qty} avg_price:{avg_price} ltp:{ltp}")
                            market_order_service.sell(token, qty)
                        if qty == max_buy_quantity and is_ltp_in_profit(ltp, avg_price, 1.5):
                            # SELL 25 percent
                            qty_to_close = get_qty_to_close(qty, max_buy_quantity)
                            logger.debug(f"sell: qty:{qty_to_close} avg_price:{avg_price} ltp:{ltp}")
                            market_order_service.sell(token, qty_to_close)
                        if qty == 3*max_buy_quantity/4 and is_ltp_in_profit(ltp, avg_price, 2):
                            # SELL another 25 percent
                            qty_to_close = get_qty_to_close(qty, max_buy_quantity)
                            logger.debug(f"sell: qty:{qty_to_close} avg_price:{avg_price} ltp:{ltp}")
                            market_order_service.sell(token, qty_to_close)
                    else:
                        logger.debug(f"no position is open !. qty:{qty}")
            time.sleep(15)
    except Exception as e:
        logger.exception("risk controller stopped.")
        telegram_bot.send(f"risk failed !! {e}")


