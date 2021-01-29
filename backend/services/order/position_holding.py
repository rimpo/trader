from injector import inject
from services.order.position import ExternalPositionService
from services.order.holding import ExternalHoldingService
from collections import defaultdict
from lib import log

class PositionHoldingService:
    """ keep track of both position and holding combined """
    @inject
    def __init__(self, logger: log.Logger, external_position_service: ExternalPositionService, external_holding_service: ExternalHoldingService):
        self.__logger = logger
        self.__external_holding_service = external_holding_service
        self.__external_position_service = external_position_service

    def get_open_position_holding(self):
        holdings = self.__external_holding_service.get_open_holding()
        positions = self.__external_position_service.get_open_position()

        open_position_holding = defaultdict(dict)
        for instrument_token, holding in holdings.items():
            quantity = holding["t1_quantity"] if holding["t1_quantity"] > 0 else holding["quantity"]
            open_position_holding[instrument_token] = {
                "average_price": holding["average_price"],
                "quantity": quantity,
                "total_value": holding["average_price"] * quantity,
            }

        for instrument_token, position in positions.items():
            self.__logger.info(f"pos_hold:{position}")
            total_value = position['total_value'] + (open_position_holding[instrument_token]["total_value"] if "total_value" in open_position_holding[instrument_token] else 0)
            open_position_holding[instrument_token]["quantity"] = position["quantity"] + (open_position_holding[instrument_token]["quantity"] if "quantity" in open_position_holding[instrument_token] else 0)
            open_position_holding[instrument_token]["average_price"] = total_value/ open_position_holding[instrument_token]["quantity"]
        return open_position_holding
