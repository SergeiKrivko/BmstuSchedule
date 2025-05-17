from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

import app.clients.lks.models as lks


class Week(StrEnum):
    ALL = "all"
    ODD = "odd"
    EVEN = "even"

    def match(self, week: Week) -> bool:
        return self in (week, Week.ALL)

    def opposite(self) -> Week:
        if self == Week.EVEN:
            return Week.ODD
        if self == Week.ODD:
            return Week.EVEN
        return Week.ALL

    @classmethod
    def from_datetime(cls, dt: datetime, current_week: Week) -> Week:
        current_week_num = datetime.now(tz=timezone.utc).isocalendar()[1]
        dt_week_num = dt.isocalendar()[1]

        if current_week_num % 2 == dt_week_num % 2:
            return current_week
        return current_week.opposite()

    @classmethod
    def from_lks(cls, week: lks.Week) -> Week:
        lks_to_domain = {
            lks.Week.ALL: cls.ALL,
            lks.Week.ODD: cls.ODD,
            lks.Week.EVEN: cls.EVEN,
        }
        return lks_to_domain.get(week, cls.ALL)

    @classmethod
    def from_lks_ru(cls, week_ru: lks.WeekRu) -> Week:
        lks_to_domain = {
            lks.WeekRu.ODD: cls.ODD,
            lks.WeekRu.EVEN: cls.EVEN,
        }
        return lks_to_domain.get(week_ru, cls.ALL)
