from flask import Flask
from flask_injector import FlaskInjector
from lib import dependencies
from lib import log
from lib.config import env
from lib.mongo_db import db
from services.api.controllers import blueprint as api_blueprint
from services.dev.controllers import blueprint as dev_blueprint


def create_app() -> Flask:
    app = Flask('Trader Rimpo Backend')
    app.register_blueprint(api_blueprint, url_prefix="/backend/api")
    app.register_blueprint(dev_blueprint)
    FlaskInjector(app=app, injector=dependencies.create_injector())
    log.initialize_root_logger()
    return app
