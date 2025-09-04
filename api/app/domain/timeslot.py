from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pydantic import BaseModel

from app.domain.errors import InvalidTimeFormatError

MOSCOW_TZ = timezone(timedelta(hours=3))


class TimeSlot(BaseModel):
    start_time: datetime
    end_time: datetime

    def is_in_range(
        self,
        dt_from: datetime,
        dt_to: datetime,
    ) -> bool:
        return not (self.end_time < dt_from or self.start_time > dt_to)

    @staticmethod
    def from_str_times(
        start_time: str,
        end_time: str,
        current_date: datetime,
    ) -> TimeSlot:
        try:
            start_hour, start_minute = map(int, start_time.split(":"))
            end_hour, end_minute = map(int, end_time.split(":"))
        except ValueError as e:
            raise InvalidTimeFormatError from e

        concrete_start = current_date.replace(
            hour=start_hour,
            minute=start_minute,
            second=0,
            microsecond=0,
            tzinfo=MOSCOW_TZ,
        )
        concrete_end = current_date.replace(
            hour=end_hour,
            minute=end_minute,
            second=0,
            microsecond=0,
            tzinfo=MOSCOW_TZ,
        )

        return TimeSlot(
            start_time=concrete_start,
            end_time=concrete_end,
        )
