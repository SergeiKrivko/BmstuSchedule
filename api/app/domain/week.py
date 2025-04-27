from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

import app.clients.lks.models as lks

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

    @classmethod
    def from_lks(cls, week: lks.Week) -> Week:
        lks_to_domain = {
            lks.Week.ALL: cls.ALL,
            lks.Week.ODD: cls.ODD,
            lks.Week.EVEN: cls.EVEN,
        }
        return lks_to_domain.get(week, cls.ALL)
