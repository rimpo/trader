import json
import logging
from .load_env import API_KEY, ACCESS_TOKEN, INSTRUMENT_FILE, EXCHANGE

from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('generate_instruments')


if __name__ == "__main__":

    kite = KiteConnect(API_KEY)
    kite.set_access_token(ACCESS_TOKEN)

    instruments = kite.instruments(EXCHANGE)
    with open(INSTRUMENT_FILE, 'w') as f:
        json.dump(instruments, f)
