from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Config:
    kite_api_key: str
    kite_api_secret: str

