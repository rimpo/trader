import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from kiteconnect import KiteTicker
from kiteconnect import KiteConnect
from config import API_KEY, ACCESS_TOKEN, INSTRUMENT_FILE

# from pytimeparse import parse
from pytz import timezone


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('generate_instruments')

def load_instrument(exchange: str) -> dict:
    with open(INSTRUMENT_FILE) as json_file:
        instruments = json.load(json_file)
        return instruments


@dataclass(frozen=True)
class Candle:
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    tick_count: int
    start_time: datetime
    last_traded_time: datetime

# 256265
# 341249
# 69121
# start_from = now - timedelta(seconds=parse(start_offset_from_now))


def converter(o):
    if isinstance(o, datetime):
        return o.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

if __name__ == "__main__":

    kite = KiteConnect(API_KEY)
    kite.set_access_token(ACCESS_TOKEN)

    india = timezone('Asia/Kolkata')
    fmt = '%Y-%m-%d %H:%M:%S'

    to_date = india.localize(datetime(2020, 12, 30, 15, 35, 0))

    #from_date = to_date - timedelta(days=1)
    from_date = india.localize(datetime(2020, 12, 30, 9, 15, 0))

    print(from_date.strftime(fmt))
    print(to_date.strftime(fmt))
    data = kite.historical_data(424961, from_date.strftime(fmt), to_date.strftime(fmt), interval="minute", continuous=False, oi=True)
    with open('./data/ITC_minute_30Dec.json', 'w') as f:
        v = json.dumps(data, default=converter)
        f.write(v)

