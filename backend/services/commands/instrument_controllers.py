from .controllers import blueprint
import click
from lib import dependencies
from lib.config import env
from lib import log
from services.instruments.instruments import InstrumentService

from flask import Blueprint

blueprint = Blueprint('instrument', __name__)

@blueprint.cli.command("download")
def create_instrument():
    injector = dependencies.create_injector()
    logger = injector.get(log.Logger)
    instrument_service = injector.get(InstrumentService)
    instrument_service.create_instruments()
    logger.info("NSE instrument download complete.")

