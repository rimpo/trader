import sys

from services.auth import AuthServiceBase
from kiteconnect import KiteConnect
from lib.config import env
from services.instruments import InstrumentService, InstrumentDummyRepository
from services.order.order import MISMarketOrderService
from services.external.kite.order.order import MarketOrderService
from services.external.kite.instrument import InstrumentService as ExternalInstrumentService
from lib.log import initialize_root_logger

import logging
import signal
import time

initialize_root_logger()
logger = logging.getLogger()


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


class AuthService(AuthServiceBase):
    def __init__(self):
        self.__kite = KiteConnect(env.KITE_API_KEY)
        self.__kite.set_access_token(env.KITE_ACCESS_TOKEN)

    def get_kite(self):
        return self.__kite


auth_service = AuthService()
external_order_service = MarketOrderService(logger, auth_service)
order_service = MISMarketOrderService(logger, external_order_service)

instrument_repo = InstrumentDummyRepository(logger)
external_instrument_service = ExternalInstrumentService(logger, auth_service)
instrument_service = InstrumentService(external_instrument_service, instrument_repo)

killer = GracefulKiller()

if len(sys.argv) < 5:
    logger.error(f"argument {sys.argv}")
    exit(0)

exchange = sys.argv[1]
symbol = sys.argv[2]  # "NIFTY2121815200PE"
qty = int(sys.argv[3])
maxloss = float(sys.argv[4])

maxloss = -1 * maxloss

order_service.buy(exchange, symbol, qty)
prices = instrument_service.get_symbol_ltp(exchange, [symbol, ])
approx_traded_price = prices[f"{exchange}:{symbol}"]["last_price"]
total_value = approx_traded_price * qty
logger.info(f"exchange:{exchange} symbol:{symbol} approx_traded_price:{approx_traded_price}")

while not killer.kill_now:
    prices = instrument_service.get_symbol_ltp(exchange, [symbol, ])
    ltp = prices[f"{exchange}:{symbol}"]["last_price"]
    profit = ltp * qty - total_value
    logger.info(f"current profit: {profit} ltp:{ltp} bought_price:{approx_traded_price}")
    if maxloss > ltp * qty - total_value:
        order_service.sell(exchange, symbol, qty)
        logger.info(f"exiting with loss: {profit}  bought_price:{approx_traded_price} :(")
        quit(0)
        break
    time.sleep(0.5)
order_service.sell(exchange, symbol, qty)
prices = instrument_service.get_symbol_ltp(exchange, [symbol, ])
ltp = prices[f"{exchange}:{symbol}"]["last_price"]
profit = ltp * qty - total_value
logger.info(f"exit with profit: {profit} ltp:{ltp} bought_price:{approx_traded_price}")


