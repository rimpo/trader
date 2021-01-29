from injector import inject
from lib import log
from typing import Dict, Protocol


class ExternalHoldingService(Protocol):
    def get_holdings(self):
        pass

    def get_open_holding(self):
        pass


class HoldingService:
    @inject
    def __init__(self, logger: log.Logger, external_holding_service: ExternalHoldingService):
        self.__external_holding_service = external_holding_service

    def get_open_holding(self) -> Dict[str, dict]:
        return self.__external_holding_service.get_open_holding()
