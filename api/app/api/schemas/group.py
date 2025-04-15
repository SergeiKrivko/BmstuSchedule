from pydantic import BaseModel, Field

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.api.schemas.response import APIResponse
from app.domain.timeslot import TimeSlot


class GroupScheduleItem(BaseModel):
    """Представляет конкретную пару расписания с конкретным временем начала и конца."""

    time_slot: TimeSlot = Field(description="Конкретное время начала и конца пары")
    teachers: list[TeacherBase] = Field(
        default_factory=list,
        description="List of teachers",
    )
    discipline: DisciplineBase = Field(description="Discipline")
    rooms: list[RoomBase] = Field(description="Rooms")


class GroupSchedule(BaseModel):
    group: GroupBase
    schedule: list[GroupScheduleItem]


class GroupList(BaseModel):
    items: list[GroupBase]
    total: int
    page: int
    size: int


class GroupListResponse(APIResponse):
    data: GroupList
    detail: str = "Groups list retrieved successfully"


class GroupResponse(APIResponse):
    data: GroupBase
    detail: str = "Group information retrieved successfully"


class GroupScheduleResponse(APIResponse):
    data: GroupSchedule
    detail: str = "Group schedule retrieved successfully"
