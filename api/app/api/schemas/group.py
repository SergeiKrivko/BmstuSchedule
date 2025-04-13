from pydantic import BaseModel, Field

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.api.schemas.response import APIResponse
from app.domain.day_of_week import DayOfWeek
from app.domain.timeslot import TimeSlot
from app.domain.week import Week


class GroupScheduleItem(BaseModel):
    day: DayOfWeek = Field(description="Day of week")
    week: Week = Field(description="Week (all, odd, even)")
    time_slot: TimeSlot = Field(description="Time slot")
    teachers: list[TeacherBase] = Field(
        default_factory=list,
        description="List of teachers",
    )
    discipline: DisciplineBase = Field(description="Discipline")
    room: RoomBase = Field(description="Room")


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
