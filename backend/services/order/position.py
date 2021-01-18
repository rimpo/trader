from injector import inject
from lib import log
from typing import Dict, Protocol


class ExternalPositionService(Protocol):
    def get_position_all(self):
        pass

    def get_open_position(self):
        pass


class PositionService:
    @inject
    def __init__(self, logger: log.Logger, external_position_service: ExternalPositionService):
        self.__external_position_service = external_position_service

    def get_open_position(self) -> Dict[str, int]:
        return self.__external_position_service.get_open_position()

    def open_position_convert_MIS_to_CNC(self):
        pass
