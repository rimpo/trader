from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Config:
    api_key: str
    api_secret: str

    def __init__(self,  api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
