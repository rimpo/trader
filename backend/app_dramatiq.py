from remodel.connection import pool
from lib.config import env
from rethinkdb import r
from remodel.connection import get_conn
import dramatiq

from lib.app_dramatiq import process_ticks


pool.configure(max_connections=5, host=env.DB_HOST, port=env.DB_PORT, auth_key=None, user=env.DB_USER, password=env.DB_PASSWORD, db=env.DB_NAME)

