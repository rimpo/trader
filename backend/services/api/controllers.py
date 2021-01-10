from flask import Blueprint, make_response, request, Response
from lib import log
from lib.config import env
from rethinkdb import r
from remodel.connection import get_conn
from services import external
from datetime import datetime
from pytz import timezone

blueprint = Blueprint("ui", __name__)


india = timezone('Asia/Kolkata')
# will need some sort of authentication !!
# blueprint.before_request(handle_authentication)

@blueprint.route('/', methods=["GET"])
def index():
    with get_conn() as conn:
        rdb.table_create('tv_shows').run(conn)
        rdb.table('tv_shows').insert({'name': 'Star Trek TNG'}).run(conn)
    return "hello"


@blueprint.route('/auth/callback', methods=["GET"])
def generate_access_token(logger: log.Logger, access_token_service: external.kite.AccessTokenService):
    status = request.args.get('status', '')
    if status == 'success':
        request_token = request.args.get('request_token', '')
        access_token = access_token_service.generate_access_token(request_token, env.KITE_API_SECRET)
        access_token_service.set_access_token(access_token)
        with get_conn() as conn:
            r.db(env.DB_NAME).table('auth').insert({"id": 1, "request_token": request_token, "access_token": access_token}, durability="hard", conflict="update").run(conn)
        return "success"
    return "failed"


@blueprint.route('/instrument/generate', methods=["GET"])
def instrument_generate(logger: log.Logger, instrument_service: external.kite.InstrumentService):
    instruments = instrument_service.get_instruments()
    for ins in instruments:
        ins['expiry'] = str(ins['expiry'])
    print(instruments[0])
    with get_conn() as conn:
        r.db(env.DB_NAME).table('instrument').insert(instruments, durability="hard", conflict="update").run(conn)
    return "success"


@blueprint.route('/instrument/ltp', methods=["GET"])
def instrument_ltp(logger: log.Logger, instrument_service: external.kite.InstrumentService):
    instruments = instrument_service.get_instruments()
    for ins in instruments:
        ins['expiry'] = str(ins['expiry'])
    print(instruments[0])
    with get_conn() as conn:
        r.db(env.DB_NAME).table('instrument').insert(instruments, durability="hard", conflict="update").run(conn)
    return "success"



