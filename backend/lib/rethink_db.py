from remodel.connection import ConnectionPool

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RethinkDB:
    pool: ConnectionPool

