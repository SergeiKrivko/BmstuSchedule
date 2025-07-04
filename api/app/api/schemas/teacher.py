from typing import Optional

from pydantic import BaseModel

from app.api.schemas.base import TeacherBase
from app.api.schemas.response import APIResponse
from app.api.schemas.schedule_pair import SchedulePairRead


class TeacherSchedule(BaseModel):
    teacher: TeacherBase
    schedule: list[SchedulePairRead]


class TeacherList(BaseModel):
    items: list[TeacherBase]
    total: int
    page: Optional[int]
    size: Optional[int]


class TeacherListResponse(APIResponse):
    data: TeacherList
    detail: str = "Teachers list retrieved successfully"


class TeacherResponse(APIResponse):
    data: TeacherBase
    detail: str = "Teacher information retrieved successfully"


class TeacherScheduleResponse(APIResponse):
    data: TeacherSchedule
    detail: str = "Teacher schedule retrieved successfully"
