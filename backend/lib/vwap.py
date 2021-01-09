from dataclasses import dataclass

@dataclass(frozen=False)
class VWAP:
    volume: int
    value: float

    def avg_price(self, candle):
        return (candle["high"] + candle["low"] + candle["close"]) / 3.0

    def calc_candle(self, candle):
        self.value = (self.value * self.volume + self.avg_price(candle) * candle["volume"]) / (self.volume + candle["volume"])
        self.volume = self.volume + candle["volume"]

    def calc_tick(self, tick):
        self.value = ((self.value * self.volume) + (tick['last_price'] * tick['last_quantity'])) / (self.volume + tick['last_quantity'])
        self.volume = self.volume + tick['last_quantity']
