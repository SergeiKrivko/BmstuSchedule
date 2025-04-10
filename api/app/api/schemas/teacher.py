from pydantic import BaseModel, Field

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.api.schemas.response import APIResponse
from app.domain.day_of_week import DayOfWeek
from app.domain.timeslot import TimeSlot


class TeacherScheduleItem(BaseModel):
    day: DayOfWeek = Field(description="Day of week")
    time_slot: TimeSlot = Field(description="Time slot")
    groups: list[GroupBase] = Field(description="List of groups")
    disciplines: list[DisciplineBase] = Field(description="List of disciplines")
    rooms: list[RoomBase] = Field(description="List of rooms")


class TeacherSchedule(BaseModel):
    teacher: TeacherBase
    schedule: list[TeacherScheduleItem]


class TeacherList(BaseModel):
    items: list[TeacherBase]
    total: int
    page: int
    size: int


class TeacherListResponse(APIResponse):
    data: TeacherList
    detail: str = "Teachers list retrieved successfully"


class TeacherResponse(APIResponse):
    data: TeacherBase
    detail: str = "Teacher information retrieved successfully"


class TeacherScheduleResponse(APIResponse):
    data: TeacherSchedule
    detail: str = "Teacher schedule retrieved successfully"
