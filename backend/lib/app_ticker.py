from typing import List
from kiteconnect import KiteTicker
from lib.config import env
# from remodel.connection import pool
# from remodel.connection import get_conn
# from lib.app_dramatiq import process_ticks
from lib import dependencies
from lib import log
import time

from rethinkdb import RethinkDB # import the RethinkDB package



def run_app():
    log.initialize_root_logger()

    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)

    logger.info("starting ticker service")

    r = RethinkDB()  # create a RethinkDB object
    conn = r.connect(host=env.DB_HOST, port=env.DB_PORT, auth_key=None, user=env.DB_USER, password=env.DB_PASSWORD, db=env.DB_NAME)

    r.db(env.DB_NAME).table('auth').wait().run(conn)
    data = r.db(env.DB_NAME).table('auth').get(1).run(conn)

    if data is not None:
        def on_ticks(ws, ticks):
            pass

        def on_connect(ws, response):
            # Callback on successful connect.
            # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
            ws.subscribe([738561, 5633])
            # Set RELIANCE to tick in `full` mode.
            ws.set_mode(ws.MODE_FULL, [738561])

        def on_close(ws, code, reason):
            # On connection close stop the main loop
            # Reconnection will not happen after executing `ws.stop()`
            ws.stop()

        kws = KiteTicker(api_key=env.KITE_API_KEY, access_token=data['access_token'])


        # Assign the callbacks.
        kws.on_ticks = on_ticks
        kws.on_connect = on_connect
        kws.on_close = on_close

        # Infinite loop on the main thread. Nothing after this will run.
        # You have to use the pre-defined callbacks to manage subscriptions.
        kws.connect(threaded=True)

        logger.info("start processing!!")
        while True:
            def on_ticks(ws, ticks):
                for tick in ticks:
                    #t = Tick(tick)
                    #token_details[tick['instrument_token']].process(t)
                    logger.info(tick)
                    pass
            kws.on_ticks = on_ticks
            time.sleep(0.1)
