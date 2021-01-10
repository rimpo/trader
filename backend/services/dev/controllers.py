from flask import Blueprint, make_response, request, Response
from lib import dependencies
from lib.config import env
from lib import log
from rethinkdb import r
from lib.rethink_db import r as rdb

blueprint = Blueprint('dev', __name__)


def __create_tables(logger: log.Logger, conn):
    # auth will store request token & access token
    r.db(env.DB_NAME).table_create('auth', primary_key='id').run(conn)

    # all the instrument downloaded from NSE
    r.db(env.DB_NAME).table_create('instrument', primary_key='instrument_token').run(conn)

@blueprint.cli.command("recreate-db")
def recreate_db():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    conn = r.connect(host=env.DB_HOST, port=env.DB_PORT, user='admin', password=env.DB_ADMIN_PASSWORD)

    # drop and create the database
    dbs = r.db_list().run(conn)
    logger.warning(dbs)
    if env.DB_NAME in dbs:
        r.db_drop(env.DB_NAME).run(conn)
    r.db_create(env.DB_NAME).run(conn)

    # drop and create the user
    user = r.db('rethinkdb').table('users').get(env.DB_USER).run(conn)
    if user is not None:
        r.db('rethinkdb').table('users').get(env.DB_USER).delete(durability="hard").run(conn)
    r.db('rethinkdb').table('users').insert({"id": env.DB_USER, "password": env.DB_PASSWORD}).run(conn)
    logger.warning(f'{env.DB_USER} user created.')

    # grant permission
    r.db(env.DB_NAME).grant(env.DB_USER, {"read": True, "write": True, "config": True}).run(conn)
    logger.warning(f'{env.DB_USER} permission granted:.')

    # create tables
    __create_tables(logger, conn)


