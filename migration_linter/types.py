from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Source:
    filename: Optional[str]
    sql: str


@dataclass(frozen=True)
class MigrationError:
    name: str
    code: str
    explanation: str
    line: Optional[int] = None
