from datetime import datetime
from enum import StrEnum


class DayOfWeek(StrEnum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    @classmethod
    def from_datetime(cls, dt: datetime) -> "DayOfWeek":
        return cls(dt.strftime("%A").lower())
