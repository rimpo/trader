import click
from lib import dependencies
from lib import log
from flask import Blueprint
from services.strategy.signal import SignalService, BUY_SIGNAL, SELL_SIGNAL
from services.strategy import MacdStrategy, Strategy
from lib.telegram_bot import TelegramBot
from typing import List
from datetime import datetime, timedelta, time as dttime
from lib.time import india
from services.historical_data.historical_data import HistoricalDataService
import time

from lib.time import TimeRange, IndiaTimeService, NSEExchangeTime, TimeSleepWait, DummyExchangeTime, \
    DummySleepWait, GermanyTimeService, DummyTimeService, DummySleepWait, ExchangeClosedToday, WaitForExchangeOpenTime

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

@blueprint.cli.command("macd-backtest-result")
@click.argument('tokens', nargs=-1)
def macd_backtest_result(tokens: List[str]):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    strategy = injector.get(Strategy)
    signal_service = injector.get(SignalService)
    signals = signal_service.get_signals(tokens[0])

    first_signal = True

    for signal in signals:
        close_price = signal["close"]
        date = signal["date"].astimezone(india)
        signal_type = signal["signal"]
        logger.info(f"date:{date} {signal_type} close:{close_price}")
        if first_signal:
            first_signal = False
            if signal_type == SELL_SIGNAL:
                continue

        if signal_type == BUY_SIGNAL:
            strategy.long_entry(close_price, 100)
        if signal_type == SELL_SIGNAL:
            strategy.long_exit(close_price, 100)
    strategy.show()

@blueprint.cli.command("macd-backtest")
@click.argument('tokens', nargs=-1)
@click.option('--interval', default=15)
def macd_backtest(tokens: List[str], interval: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    macd_strategy = injector.get(MacdStrategy)

    # NOTE: MACD CALCULATION START DATETIME
    start_date = india.localize(datetime(2020, 8, 1, 9, 10, 0))

    time_range = TimeRange(
        interval=interval,
        time_service=DummyTimeService(start_date, 1),
        exchange_time=NSEExchangeTime(),
        time_wait=DummySleepWait()
    )

    try:
        for for_date in time_range.get_next():
            if for_date > datetime.utcnow().astimezone(india):
                break
            macd_strategy.run_for_date(tokens, interval, for_date)
    except Exception as e:
        logger.exception("macd strategy stopped with error.")
        return

    logger.info("macd backtest completed.")


@blueprint.cli.command("macd")
@click.argument('tokens', nargs=-1)
@click.option('--interval', default=15)
@click.option('--sleep-seconds', default=10)
@click.option('--since', default="5d")
def macd(tokens: List[str], interval: int, sleep_seconds: int, since: str):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    wait_for_exchange = WaitForExchangeOpenTime(logger, NSEExchangeTime())
    wait_for_exchange.wait_till(dttime(hour=8, minute=45))

    macd_strategy = injector.get(MacdStrategy)
    telegram_bot = injector.get(TelegramBot)

    logger.info(f"macd strategy starting for token {tokens}.")

    try:
        macd_strategy.run(tokens, interval, sleep_seconds, since)
    except ExchangeClosedToday as e:
        telegram_bot.send(f"market is closed message:{e.message}!!")
    except Exception as e:
        logger.exception("strategy failed")
        telegram_bot.send(f"strategy failed !! {e}")
    logger.info("macd strategy stopped.")

@blueprint.cli.command("test-strategy")
def test_strategy():
    injector = dependencies.create_injector()
    macd_strategy = injector.get(MacdStrategy)
    logger = injector.get(log.Logger)
    logger.info("waiting to stop")
    time.sleep(5)
    logger.info("restarting")
