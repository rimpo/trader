from lib.config import env
from rethinkdb import r

rdb = r.db(env.DB_NAME)



