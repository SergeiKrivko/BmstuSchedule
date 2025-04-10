from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field, HttpUrl

from app.domain.day_of_week import DayOfWeek
from app.domain.timeslot import TimeSlot

if TYPE_CHECKING:
    from app.api.schemas.group import DisciplineBase, GroupBase
    from app.api.schemas.teacher import TeacherBase


class RoomBase(BaseModel):
    id: int = Field(description="Room ID")
    name: str = Field(description="Room name", examples=["91"])
    building: Optional[str] = Field(
        None,
        description="Building name",
        examples=["Химлаб"],
    )
    map_url: Optional[HttpUrl] = Field(
        None,
        description="URL with room in query params of interactive map",
        examples=["https://map.mf.bmstu.ru/?location=room-91"],
    )


class RoomScheduleItem(BaseModel):
    day: DayOfWeek = Field(description="Day of week")
    time_slot: TimeSlot = Field(description="Time slot")
    groups: list["GroupBase"] = Field(
        description="List of groups in room",
    )
    teachers: list["TeacherBase"] = Field(
        description="List of teachers in room",
    )
    disciplines: list["DisciplineBase"] = Field(
        description="List of disciplines in room",
    )


class RoomSchedule(BaseModel):
    room: RoomBase
    schedule: list[RoomScheduleItem]


class RoomList(BaseModel):
    items: list[RoomBase]
    total: int
    page: int
    size: int
