from flask import Blueprint, make_response, request, Response
from lib import log
from lib.config import env
#from lib.rethink_db import RethinkDB
from rethinkdb import r
from remodel.connection import get_conn


blueprint = Blueprint("ui", __name__)

# will need some sort of authentication !!
# blueprint.before_request(handle_authentication)

@blueprint.route('/', methods=["GET"])
def index():
    with get_conn() as conn:
        r.db(env.DB_NAME).table_create('tv_shows').run(conn)
        r.table('tv_shows').insert({'name': 'Star Trek TNG'}).run(conn)
    return "hello"


@blueprint.route('/auth/callback', methods=["GET"])
def generate_access_token(logger: log.Logger):
    status = request.args.get('status', '')
    if status == 'success':
        request_token = request.args.get('request_token', '')
        logger.info(f"request_token: {request_token}")
        return "success"
    return "failed"


