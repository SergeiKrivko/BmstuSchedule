from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query

from app.api.schemas.group import (
    GroupListResponse,
    GroupResponse,
    GroupScheduleResponse,
)

router = APIRouter()


@router.get(
    "/groups",
    tags=["groups"],
    summary="Get list of groups",
    response_model=GroupListResponse,
)
async def get_groups(
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
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
) -> GroupListResponse:
    raise NotImplementedError


@router.get(
    "/groups/{group_id}",
    tags=["groups"],
    summary="Get a specific group by ID",
    response_model=GroupResponse,
)
async def get_group(
    group_id: Annotated[int, Path(description="ID of the group")],
) -> GroupResponse:
    raise NotImplementedError


@router.get(
    "/{group_id}/schedule",
    tags=["groups"],
    summary="Get schedule for a specific group",
    response_model=GroupScheduleResponse,
)
async def get_group_schedule(
    group_id: int = Path(description="ID of the group"),
    dt_from: Annotated[Optional[datetime], Query(description="Start datetime")] = None,
    dt_to: Annotated[Optional[datetime], Query(description="End datetime")] = None,
) -> GroupScheduleResponse:
    raise NotImplementedError
