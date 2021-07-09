from injector import inject
from typing import Protocol, List, Dict


class ExternalInstrumentService(Protocol):
    def get_instruments(self):
        pass

    def get_ltp(self, symbols: List[str]):
        pass

    def get_symbol_ltp(self, exchange: str, symbols: List[str]):
        pass


class InstrumentRepository(Protocol):
    def insert_instruments(self):
        pass

    def get_symbol(self, token: int) -> str:
        pass

    def get_token(self, symbol: str) -> str:
        pass


class InstrumentDummyRepository(InstrumentRepository):
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

    def __assert_invalid_price(self):
        pass

    def get_ltp(self, tokens: List[int]) -> Dict[int, float]:
        prices = self.__external_instrument_service.get_ltp([self.get_symbol(token) for token in tokens])
        return {price['instrument_token'] : price['last_price'] for _, price in prices.items()}

    def get_symbol_ltp(self, exchange: str, symbols: List[str]):
        return self.__external_instrument_service.get_symbol_ltp(exchange, symbols)
