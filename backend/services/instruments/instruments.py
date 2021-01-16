from services.external.kite.instrument import InstrumentService as ExternalInstrumentService
from injector import inject
from typing import Protocol


class InstrumentRepository(Protocol):
    def insert_instruments(self):
        pass

    def get_symbol(self, token: int) -> str:
        pass

    def get_token(self, symbol: str) -> str:
        pass


class InstrumentService:
    @inject
    def __init__(self, external_instrument_service: ExternalInstrumentService, repository: InstrumentRepository):
        self.__external_instrument_service = external_instrument_service
        self.__repository = repository

    def create_instruments(self):
        instruments = self.__external_instrument_service.get_instruments()
        if len(instruments) > 0:
            self.__repository.insert_instruments(instruments)

    def get_symbol(self, token: int):
        return self.__repository.get_symbol(token)

    def get_token(self, symbol: int):
        return self.__repository.get_token(symbol)
