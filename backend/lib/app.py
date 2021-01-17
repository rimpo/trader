from flask import Flask
from flask_injector import FlaskInjector
from lib import dependencies
from lib import log
from lib.config import env
from lib.mongo_db import db
from services.api.controllers import blueprint as api_blueprint
from services.commands.historical_data_controllers import blueprint as historical_data_blueprint
from services.commands.instrument_controllers import blueprint as instrument_blueprint
from services.commands.order_controllers import blueprint as order_blueprint
from services.commands.strategy_controllers import blueprint as strategy_blueprint
from services.commands.risk_controllers import blueprint as risk_blueprint

def create_app() -> Flask:
    app = Flask('Trader Rimpo Backend')
    app.register_blueprint(api_blueprint, url_prefix="/backend/api")
    app.register_blueprint(historical_data_blueprint)
    app.register_blueprint(instrument_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(strategy_blueprint)
    app.register_blueprint(risk_blueprint)
    FlaskInjector(app=app, injector=dependencies.create_injector())
    log.initialize_root_logger()
    return app
