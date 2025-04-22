from datetime import datetime
from enum import StrEnum

from app.clients.lks.models import Day


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

    @classmethod
    def from_lks(cls, day: Day) -> "DayOfWeek":
        all_days_of_week = (
            cls.MONDAY,
            cls.TUESDAY,
            cls.WEDNESDAY,
            cls.THURSDAY,
            cls.FRIDAY,
            cls.SATURDAY,
            cls.SUNDAY,
        )
        return all_days_of_week[day - 1]
