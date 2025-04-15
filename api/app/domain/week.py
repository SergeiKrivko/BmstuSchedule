from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


class Week(StrEnum):
    ALL = "all"
    ODD = "odd"
    EVEN = "even"

    def match(self, week: Week) -> bool:
        return self in (week, Week.ALL)

    @classmethod
    def from_datetime(cls, dt: datetime) -> Week:
        return cls.ODD if dt.isocalendar()[1] % 2 == 1 else cls.EVEN
