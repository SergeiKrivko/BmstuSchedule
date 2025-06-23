from typing import Optional

from pydantic import BaseModel

from app.api.schemas.base import RoomBase
from app.api.schemas.response import APIResponse
from app.api.schemas.schedule_pair import SchedulePairRead


class RoomSchedule(BaseModel):
    room: RoomBase
    schedule: list[SchedulePairRead]


class RoomList(BaseModel):
    items: list[RoomBase]
    total: int
    page: Optional[int]
    size: Optional[int]


class RoomListResponse(APIResponse):
    data: RoomList
    detail: str = "Rooms list retrieved successfully"


class RoomResponse(APIResponse):
    data: RoomBase
    detail: str = "Room information retrieved successfully"


class RoomScheduleResponse(APIResponse):
    data: RoomSchedule
    detail: str = "Room schedule retrieved successfully"
