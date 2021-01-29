from injector import inject
from services.order.position import ExternalPositionService
from services.order.holding import ExternalHoldingService
from collections import defaultdict

class PositionHoldingService:
    """ keep track of both position and holding combined """
    @inject
    def __init__(self, external_position_service: ExternalPositionService, external_holding_service: ExternalHoldingService):
        self.__external_holding_service = external_holding_service
        self.__external_position_service = external_position_service

    def get_open_position_holding(self):
        holdings = self.__external_holding_service.get_open_holding()
        positions = self.__external_holding_service.get_open_holding()

        open_position_holding = defaultdict(dict)
        for instrument_token, holding in holdings.items():
            open_position_holding[instrument_token] = {
                "average_price": holding["average_price"],
                "quantity": holding["t1_quantity"] if holding["t1_quantity"] > 0 else holding["quantity"]
            }

        for instrument_token, position in positions.items():
            average_price = (position['average_price'] + open_position_holding[instrument_token]["average_price"] if "average_price" in open_position_holding[instrument_token] else position['average_price'])/2.0
            open_position_holding[instrument_token]["average_price"] = average_price
            open_position_holding[instrument_token]["quantity"] += position["quantity"]
        return open_position_holding
