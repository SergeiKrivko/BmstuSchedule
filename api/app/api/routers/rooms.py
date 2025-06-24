from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query

from app.api.schemas.room import (
    RoomListResponse,
    RoomResponse,
    RoomScheduleResponse,
)
from app.db.database import SessionMakerDep
from app.services.room_svc import RoomSvcDep

router = APIRouter()


@router.get(
    "/rooms",
    tags=["rooms"],
    summary="Get list of rooms",
    response_model=RoomListResponse,
)
async def get_rooms(
    sessionmaker: SessionMakerDep,
    room_svc: RoomSvcDep,
    building: Annotated[
        Optional[str],
        Query(description="Filter rooms by building"),
    ] = None,
    page: Annotated[Optional[int], Query(ge=1, description="Page number")] = None,
    size: Annotated[Optional[int], Query(ge=1, le=100, description="Page size")] = None,
) -> RoomListResponse:
    rooms = await room_svc.get_rooms(
        sessionmaker=sessionmaker,
        building=building,
        page=page,
        size=size,
    )
    return RoomListResponse(data=rooms)


@router.get(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Get a specific room by ID",
    response_model=RoomResponse,
)
async def get_room(
    sessionmaker: SessionMakerDep,
    room_svc: RoomSvcDep,
    room_id: Annotated[int, Path(description="ID of the room")],
) -> RoomResponse:
    room = await room_svc.get_room(
        sessionmaker=sessionmaker,
        room_id=room_id,
    )
    return RoomResponse(data=room)


@router.get(
    "/rooms/{room_id}/schedule",
    tags=["rooms"],
    summary="Get schedule for a specific room",
    response_model=RoomScheduleResponse,
)
async def get_room_schedule(
    sessionmaker: SessionMakerDep,
    room_svc: RoomSvcDep,
    room_id: Annotated[int, Path(description="ID of the room")],
    dt_from: Annotated[datetime, Query(description="Start datetime")],
    dt_to: Annotated[datetime, Query(description="End datetime")],
) -> RoomScheduleResponse:
    room_schedule = await room_svc.get_room_schedule(
        sessionmaker=sessionmaker,
        room_id=room_id,
        dt_from=dt_from,
        dt_to=dt_to,
    )
    return RoomScheduleResponse(data=room_schedule)


@router.get(
    "/rooms/free",
    tags=["rooms"],
    summary="Get list of rooms that are free during the specified time period",
    response_model=RoomListResponse,
)
async def get_free_rooms(
    sessionmaker: SessionMakerDep,
    room_svc: RoomSvcDep,
    dt_from: Annotated[datetime, Query(description="Start datetime")],
    dt_to: Annotated[datetime, Query(description="End datetime")],
    building: Annotated[
        Optional[str],
        Query(description="Filter rooms by building"),
    ] = None,
) -> RoomListResponse:
    raise NotImplementedError
