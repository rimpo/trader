
from flask import Blueprint, make_response, request, Response
from lib import log
from lib.config import env
from services import external
from datetime import datetime
from pytz import timezone
from kiteconnect import KiteConnect
from services.auth import auth

blueprint = Blueprint("ui", __name__)

india = timezone('Asia/Kolkata')
# will need some sort of authentication !!
# blueprint.before_request(handle_authentication)

@blueprint.route('/', methods=["GET"])
def index():
    return "hello"


@blueprint.route('/auth/callback', methods=["GET"])
def auth_callback(logger: log.Logger, auth_service: auth.AuthService):
    status = request.args.get('status', '')
    if status == 'success':
        request_token = request.args.get('request_token', '')
        auth_service.generate_access_token(request_token)
        return "success"
    return "failed"


@blueprint.route('/order/callback', methods=["POST"])
def order_callback(logger: log.Logger):
    logger.info(request.json)
    logger.info(request.args)
    logger.info(request.data)
    return "success"


@blueprint.route('/instrument/generate', methods=["GET"])
def instrument_generate(logger: log.Logger, instrument_service: external.kite.InstrumentService):
    instruments = instrument_service.get_instruments()
    for ins in instruments:
        ins['expiry'] = str(ins['expiry'])
    print(instruments[0])
    return "success"


@blueprint.route('/candles/historical_data/download', methods=["GET"])
def historical_data(logger: log.Logger, kite: KiteConnect):
    india = timezone('Asia/Kolkata')
    to_date = india.localize(datetime(2020, 1, 11, 15, 35, 0))
    from_date = india.localize(datetime(2020, 1, 1, 9, 15, 0))
    # from_date = to_date - timedelta(days=1)
    fmt = '%Y-%m-%d %H:%M:%S'
    # #print(from_date.strftime(fmt))
    # print(to_date.strftime(fmt))
    results = kite.historical_data(424961, from_date.strftime(fmt), to_date.strftime(fmt), interval="5minute",
                                continuous=False, oi=True)

    for data in results:
        data['date'] = india.localize(data['date'])

    return "success"




