from pydantic import BaseModel, Field

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.api.schemas.response import APIResponse
from app.domain.day_of_week import DayOfWeek
from app.domain.timeslot import TimeSlot


class RoomScheduleItem(BaseModel):
    day: DayOfWeek = Field(description="Day of week")
    time_slot: TimeSlot = Field(description="Time slot")
    groups: list[GroupBase] = Field(
        description="List of groups in room",
    )
    teachers: list[TeacherBase] = Field(
        description="List of teachers in room",
    )
    disciplines: list[DisciplineBase] = Field(
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


class RoomListResponse(APIResponse):
    data: RoomList
    detail: str = "Rooms list retrieved successfully"


class RoomResponse(APIResponse):
    data: RoomBase
    detail: str = "Room information retrieved successfully"


class RoomScheduleResponse(APIResponse):
    data: RoomSchedule
    detail: str = "Room schedule retrieved successfully"
