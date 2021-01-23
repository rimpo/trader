import click
from lib import dependencies
from lib import log
from flask import Blueprint
from services.strategy.signal import SignalService, BUY_SIGNAL, SELL_SIGNAL
from services.strategy import MacdStrategy, Strategy
from lib.telegram_bot import TelegramBot
from typing import List
from datetime import datetime, timedelta
from lib.time import india
from services.historical_data.historical_data import HistoricalDataService

from lib.time import TimeRange, IndiaTimeService, NSEExchangeTime, TimeSleepWait, DummyExchangeTime, \
    DummySleepWait, GermanyTimeService, DummyTimeService, DummySleepWait

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
    telegram_bot = injector.get(TelegramBot)
    historical_data_service = injector.get(HistoricalDataService)
    strategy = injector.get(Strategy)
    signal_service = injector.get(SignalService)

    # NOTE: HISTORICAL DOWNLOAD DATETIME
    from_date = india.localize(datetime(2020, 9, 1, 9, 10, 0))
    to_date = india.localize(datetime(2021, 1, 22, 9, 10, 0))

    for token in tokens:
        historical_data_service.download_and_save(token, interval, from_date, to_date)

    logger.info(f"historical data download for_date:{from_date} to_date:{to_date} tokens:{tokens}.")

    # NOTE: MACD CALCULATION START DATETIME
    start_date = india.localize(datetime(2020, 9, 5, 9, 10, 0))

    time_range = TimeRange(
        interval=interval,
        time_service=DummyTimeService(start_date, 1),
        exchange_time=NSEExchangeTime(),
        time_wait=DummySleepWait()
    )

    try:
        for for_date in time_range.get_next():
            macd_strategy.run_for_date_nowait(tokens, interval, for_date)

        signals = signal_service.get_signals(tokens[0])

        first_signal = True

        for signal in signals:
            close_price = signal["close"]
            date = signal["date"]
            signal_type = signal["signal"]
            logger.info(f"date:{date} {signal_type} close:{close_price}")
            if first_signal and signal_type == SELL_SIGNAL:
                continue

            if signal_type == BUY_SIGNAL:
                strategy.long_entry(close_price, 100)
            if signal_type == SELL_SIGNAL:
                strategy.long_exit(close_price, 100)
        strategy.show()

    except Exception as e:
        logger.exception("macd strategy stopped.")
        telegram_bot.send(f"strategy-backtest failed !! {e}")

    logger.info("macd backtest completed.")


@blueprint.cli.command("macd")
@click.argument('tokens', nargs=-1)
@click.option('--interval', default=15)
def macd(tokens: List[str], interval: int):
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    macd_strategy = injector.get(MacdStrategy)
    telegram_bot = injector.get(TelegramBot)

    logger.info(f"macd strategy starting for token {tokens}.")
    time_range = TimeRange(interval=interval, time_service=IndiaTimeService(), exchange_time=NSEExchangeTime(),
                           time_wait=TimeSleepWait(seconds=15))
    try:
        for for_date in time_range.get_next():
            macd_strategy.run(tokens, interval, for_date)
    except Exception as e:
        logger.exception("macd strategy stopped.")
        telegram_bot.send(f"strategy failed !! {e}")

    logger.info("macd strategy stopped.")


