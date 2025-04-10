from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Query

from app.api.schemas.response import APIResponse
from app.api.schemas.room import RoomBase, RoomList, RoomSchedule
from app.domain.day_of_week import DayOfWeek

router = APIRouter()


@router.get(
    "/rooms",
    tags=["rooms"],
    summary="Get list of rooms",
    response_model=APIResponse[RoomList],
)
async def get_rooms(
    building: Annotated[
        Optional[str],
        Query(description="Filter rooms by building"),
    ] = None,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
) -> APIResponse[RoomList]:
    raise NotImplementedError


@router.get(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Get a specific room by ID",
    response_model=APIResponse[RoomBase],
)
async def get_room(room_id: int) -> APIResponse[RoomBase]:
    raise NotImplementedError


@router.get(
    "/rooms/{room_id}/schedule",
    tags=["rooms"],
    summary="Get schedule for a specific room",
    response_model=APIResponse[RoomSchedule],
)
async def get_room_schedule(
    room_id: int,
    day: Annotated[Optional[DayOfWeek], Query(description="Day of week")] = None,
    dt_from: Annotated[Optional[datetime], Query(description="Start datetime")] = None,
    dt_to: Annotated[Optional[datetime], Query(description="End datetime")] = None,
) -> APIResponse[RoomSchedule]:
    raise NotImplementedError


@router.get(
    "/rooms/free",
    tags=["rooms"],
    summary="Get list of rooms that are free during the specified time period",
    response_model=APIResponse[RoomList],
)
async def get_free_rooms(
    dt_from: Annotated[datetime, Query(description="Start datetime")],
    dt_to: Annotated[datetime, Query(description="End datetime")],
    building: Annotated[
        Optional[str],
        Query(description="Filter rooms by building"),
    ] = None,
) -> APIResponse[RoomList]:
    raise NotImplementedError
