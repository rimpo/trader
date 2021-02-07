from injector import inject
from lib import log
from typing import Protocol, List
from dataclasses import dataclass


@dataclass(frozen=True)
class OpenPosition:
    symbol: str
    exchange: str
    instrument_token: str
    average_price: float
    quantity: int


class ExternalPositionService(Protocol):
    def get_position_all(self):
        pass

    def get_open_position(self):
        pass


class PositionService:
    @inject
    def __init__(self, logger: log.Logger, external_position_service: ExternalPositionService):
        self.__external_position_service = external_position_service

    def get_open_position(self) -> List[OpenPosition]:
        return self.__external_position_service.get_open_position()

