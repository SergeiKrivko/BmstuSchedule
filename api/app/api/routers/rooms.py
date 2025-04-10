from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query

from app.api.schemas.room import (
    RoomListResponse,
    RoomResponse,
    RoomScheduleResponse,
)
from app.domain.day_of_week import DayOfWeek

router = APIRouter()


@router.get(
    "/rooms",
    tags=["rooms"],
    summary="Get list of rooms",
    response_model=RoomListResponse,
)
async def get_rooms(
    building: Annotated[
        Optional[str],
        Query(description="Filter rooms by building"),
    ] = None,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
) -> RoomListResponse:
    raise NotImplementedError


@router.get(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Get a specific room by ID",
    response_model=RoomResponse,
)
async def get_room(
    room_id: Annotated[int, Path(description="ID of the room")],
) -> RoomResponse:
    raise NotImplementedError


@router.get(
    "/rooms/{room_id}/schedule",
    tags=["rooms"],
    summary="Get schedule for a specific room",
    response_model=RoomScheduleResponse,
)
async def get_room_schedule(
    room_id: Annotated[int, Path(description="ID of the room")],
    day: Annotated[Optional[DayOfWeek], Query(description="Day of week")] = None,
    dt_from: Annotated[Optional[datetime], Query(description="Start datetime")] = None,
    dt_to: Annotated[Optional[datetime], Query(description="End datetime")] = None,
) -> RoomScheduleResponse:
    raise NotImplementedError


@router.get(
    "/rooms/free",
    tags=["rooms"],
    summary="Get list of rooms that are free during the specified time period",
    response_model=RoomListResponse,
)
async def get_free_rooms(
    dt_from: Annotated[datetime, Query(description="Start datetime")],
    dt_to: Annotated[datetime, Query(description="End datetime")],
    building: Annotated[
        Optional[str],
        Query(description="Filter rooms by building"),
    ] = None,
) -> RoomListResponse:
    raise NotImplementedError
