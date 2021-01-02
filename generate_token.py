import logging
from config import API_KEY, REQUEST_TOKEN, API_SECRET
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('generate_token')


if __name__ == "__main__":
    if len(API_KEY) < 5:
        logger.error("Invalid API_KEY")
        quit()

    if len(REQUEST_TOKEN) < 5:
        logger.error("Invalid REQUEST_TOKEN")
        quit()

    if len(API_SECRET) < 5:
        logger.error("Invalid API_SECRET")
        quit()

    kite = KiteConnect(API_KEY)
    data = kite.generate_session(REQUEST_TOKEN, API_SECRET)
    logger.info(data["access_token"])
