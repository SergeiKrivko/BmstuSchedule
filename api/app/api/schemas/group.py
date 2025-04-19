from pydantic import BaseModel

from app.api.schemas.base import GroupBase
from app.api.schemas.response import APIResponse
from app.models import SchedulePair


class GroupSchedule(BaseModel):
    group: GroupBase
    schedule: list[SchedulePair]


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
