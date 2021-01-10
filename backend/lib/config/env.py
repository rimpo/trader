import os


PRODUCTION = "production"
DEVELOPMENT = "development"
TESTING = "testing"

TRADER_RIMPO_ENV = os.environ["TRADER_RIMPO_ENV"]

KITE_API_KEY = os.environ["KITE_API_KEY"]
KITE_API_SECRET = os.environ["KITE_API_SECRET"]

# KITE_REQUEST_TOKEN = os.environ["KITE_REQUEST_TOKEN"]
# KITE_ACCESS_TOKEN = os.environ["KITE_ACCESS_TOKEN"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_ADMIN_PASSWORD = os.environ["DB_ADMIN_PASSWORD"]
# EXCHANGE = os.environ["EXCHANGE"]

INSTRUMENT_FILE = "./data/instruments.json"

TRADER_RIMPO_BOT_ACCESS_TOKEN = os.environ["TRADER_RIMPO_BOT_ACCESS_TOKEN"]
