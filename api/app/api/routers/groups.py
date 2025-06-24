from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query

from app.api.schemas.group import (
    GroupListResponse,
    GroupResponse,
    GroupScheduleResponse,
)
from app.db.database import SessionMakerDep
from app.services.group_svc import GroupSvcDep

router = APIRouter()


@router.get(
    "/groups",
    tags=["groups"],
    summary="Get list of groups",
    response_model=GroupListResponse,
)
async def get_groups(
    sessionmaker: SessionMakerDep,
    group_svc: GroupSvcDep,
    abbr: Annotated[
        Optional[str],
        Query(description="Filter groups by abbreviation"),
    ] = None,
    course: Annotated[
        Optional[str],
        Query(description="Filter groups by course abbreviation"),
    ] = None,
    department: Annotated[
        Optional[str],
        Query(description="Filter groups by department abbreviation"),
    ] = None,
    faculty: Annotated[
        Optional[str],
        Query(description="Filter groups by faculty abbreviation"),
    ] = None,
    filial: Annotated[
        Optional[str],
        Query(description="Filter groups by filial abbreviation"),
    ] = None,
    page: Annotated[Optional[int], Query(ge=1, description="Page number")] = None,
    size: Annotated[Optional[int], Query(ge=1, le=100, description="Page size")] = None,
) -> GroupListResponse:
    groups = await group_svc.get_groups(
        sessionmaker,
        abbr=abbr,
        course=course,
        department=department,
        faculty=faculty,
        filial=filial,
        page=page,
        size=size,
    )
    return GroupListResponse(data=groups)


@router.get(
    "/groups/{group_id}",
    tags=["groups"],
    summary="Get a specific group by ID",
    response_model=GroupResponse,
)
async def get_group(
    sessionmaker: SessionMakerDep,
    group_svc: GroupSvcDep,
    group_id: Annotated[int, Path(description="ID of the group")],
) -> GroupResponse:
    group = await group_svc.get_group(sessionmaker, group_id)
    return GroupResponse(data=group)


@router.get(
    "/groups/{group_id}/schedule",
    tags=["groups"],
    summary="Get schedule for a specific group",
    response_model=GroupScheduleResponse,
)
async def get_group_schedule(
    sessionmaker: SessionMakerDep,
    group_svc: GroupSvcDep,
    group_id: Annotated[int, Path(description="ID of the group")],
    dt_from: Annotated[datetime, Query(description="Start datetime")],
    dt_to: Annotated[datetime, Query(description="End datetime")],
) -> GroupScheduleResponse:
    schedule = await group_svc.get_group_schedule(
        sessionmaker=sessionmaker,
        group_id=group_id,
        dt_from=dt_from,
        dt_to=dt_to,
    )
    return GroupScheduleResponse(data=schedule)
