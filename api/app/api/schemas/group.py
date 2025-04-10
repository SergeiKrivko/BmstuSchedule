from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

from app.domain.day_of_week import DayOfWeek
from app.domain.timeslot import TimeSlot
from app.domain.week import Week

if TYPE_CHECKING:
    from app.api.schemas.room import RoomBase
    from app.api.schemas.teacher import TeacherBase


class DisciplineBase(BaseModel):
    id: int = Field(description="Discipline ID")
    full_name: str = Field(
        description="Discipline full name",
        examples=["Интегралы и дифференциальные уравнения"],
    )
    short_name: str = Field(
        description="Discipline short name",
        examples=["ИиДУ"],
    )
    act_type: Optional[str] = Field(
        None,
        description="Discipline act type",
        examples=["seminar"],
    )


class GroupBase(BaseModel):
    id: int = Field(description="Group ID")
    abbr: str = Field(description="Group abbreviation")
    course_id: int = Field(description="Course ID")
    semester_num: int = Field(description="Semester number")


class GroupScheduleItem(BaseModel):
    day: DayOfWeek = Field(description="Day of week")
    week: Week = Field(description="Week (all, odd, even)")
    time_slot: TimeSlot = Field(description="Time slot")
    teachers: list["TeacherBase"] = Field(
        default_factory=list,
        description="List of teachers",
    )
    discipline: DisciplineBase = Field(description="Discipline")
    room: "RoomBase" = Field(description="Room")


class GroupSchedule(BaseModel):
    group: GroupBase
    schedule: list[GroupScheduleItem]


class GroupList(BaseModel):
    items: list[GroupBase]
    total: int
    page: int
    size: int
