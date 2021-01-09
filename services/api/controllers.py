from flask import Blueprint, make_response, request, Response
from lib import log

blueprint = Blueprint("ui", __name__)

# will need some sort of authentication !!
# blueprint.before_request(handle_authentication)

@blueprint.route('/', methods=["GET"])
def index():
    return "ok test."

@blueprint.route('/auth/callback', methods=["GET"])
def generate_access_token(logger: log.Logger):
    status = request.args.get('status', '')
    if status == 'success':
        request_token = request.args.get('request_token', '')
        logger.info(f"request_token: {request_token}")
        return "success"
    return "failed"


