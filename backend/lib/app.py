from flask import Flask
from flask_injector import FlaskInjector
from lib import dependencies
from lib import log
from lib.config import env
from remodel.connection import pool

from services.api.controllers import blueprint as api_blueprint
from services.dev.controllers import blueprint as dev_blueprint

def create_app() -> Flask:
    app = Flask('Trader Rimpo Backend')
    pool.configure(max_connections=5, host=env.DB_HOST, port=env.DB_PORT, auth_key=None, user=env.DB_USER, password=env.DB_PASSWORD, db=env.DB_NAME)
    app.register_blueprint(api_blueprint, url_prefix="/backend/api")
    app.register_blueprint(dev_blueprint)
    FlaskInjector(app=app, injector=dependencies.create_injector())
    log.initialize_root_logger()
    return app
