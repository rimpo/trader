from flask import Flask
from flask_injector import FlaskInjector
from lib import dependencies
from lib import log

from services.api.controllers import blueprint as api_blueprint


def create_app() -> Flask:
    app = Flask('Trader Rimpo Backend')
    app.register_blueprint(api_blueprint, url_prefix="/backend/api")
    FlaskInjector(app=app, injector=dependencies.create_injector())
    log.initialize_root_logger()
    return app
