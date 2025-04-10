from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from app.domain.day_of_week import DayOfWeek
from app.domain.timeslot import TimeSlot

if TYPE_CHECKING:
    from app.api.schemas.group import DisciplineBase, GroupBase
    from app.api.schemas.room import RoomBase


class TeacherBase(BaseModel):
    id: int = Field(description="Teacher ID")
    first_name: str = Field(description="Teacher first name", examples=["Наталья"])
    middle_name: str = Field(description="Teacher middle name", examples=["Юрьевна"])
    last_name: str = Field(description="Teacher last name", examples=["Рязанова"])

    departments: list[str] = Field(
        description="List of department abbreviations where teacher works",
        examples=["ИУ7"],
    )


class TeacherScheduleItem(BaseModel):
    day: DayOfWeek = Field(description="Day of week")
    time_slot: TimeSlot = Field(description="Time slot")
    groups: list["GroupBase"] = Field(description="List of groups")
    disciplines: list["DisciplineBase"] = Field(description="List of disciplines")
    rooms: list["RoomBase"] = Field(description="List of rooms")


class TeacherSchedule(BaseModel):
    teacher: TeacherBase
    schedule: list[TeacherScheduleItem]


class TeacherList(BaseModel):
    items: list[TeacherBase]
    total: int
    page: int
    size: int
