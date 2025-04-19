from pydantic import BaseModel

from app.api.schemas.base import TeacherBase
from app.api.schemas.response import APIResponse
from app.api.schemas.schedule_pair import SchedulePair


class TeacherSchedule(BaseModel):
    teacher: TeacherBase
    schedule: list[SchedulePair]


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
