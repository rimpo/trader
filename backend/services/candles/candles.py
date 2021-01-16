from typing import List, Protocol
from injector import inject

class CandleRepository(Protocol):
    def get_candles(self, token: int, period: str, length: int) -> List[dict]:
        pass

    def write_candles(self, token: int, period: str, data: dict):
        pass


class CandleService:
    @inject
    def __init__(self, candle_repo: CandleRepository):
        self.__candle_repo = candle_repo

    def get_candles(self, token: int, period: str, length: int) -> List[dict]:
        return self.__candle_repo.get_candles(token, period, length)

    def write_candles(self, token: int, period: str, data: dict):
        self.__candle_repo.write_candles(token, period, data)
