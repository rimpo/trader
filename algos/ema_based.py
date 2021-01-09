import json
import logging
from datetime import datetime
from dataclasses import dataclass
from kiteconnect import KiteTicker
#from kiteconnect import KiteConnect
from config import API_KEY, ACCESS_TOKEN, INSTRUMENT_FILE


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('generate_instruments')


subscribed_tokens = [256265, ]
#kite = KiteConnect(API_KEY)
#kite.set_access_token(ACCESS_TOKEN)

kws = KiteTicker(API_KEY, ACCESS_TOKEN)

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    logging.debug("Ticks: {}".format(ticks))

def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe(subscribed_tokens)

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, subscribed_tokens)
    logger.info(f"token: {subscribed_tokens} subscribed")

def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()
    logger.error("on_close called")

def on_reconnect(ws, attemps_count):
    logger.warning(f"reconnect attempt {attemps_count}")

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()

