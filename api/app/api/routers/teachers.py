from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Query

from app.api.schemas.response import APIResponse
from app.api.schemas.teacher import TeacherBase, TeacherList, TeacherSchedule

router = APIRouter()


@router.get(
    "/teachers",
    tags=["teachers"],
    summary="Get list of teachers",
    response_model=APIResponse[TeacherList],
)
async def get_teachers(
    name: Annotated[
        Optional[str],
        Query(None, description="Filter teachers by any part of full name"),
    ] = None,
    department: Annotated[
        Optional[str],
        Query(
            None,
            description="Filter teachers by department abbreviation",
        ),
    ] = None,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
) -> APIResponse[TeacherList]:
    raise NotImplementedError


@router.get(
    "/teachers/{teacher_id}",
    tags=["teachers"],
    summary="Get a specific teacher by ID",
    response_model=APIResponse[TeacherBase],
)
async def get_teacher(teacher_id: int) -> APIResponse[TeacherBase]:
    raise NotImplementedError


@router.get(
    "/teachers/{teacher_id}/schedule",
    tags=["teachers"],
    summary="Get schedule for a specific teacher",
    response_model=APIResponse[TeacherSchedule],
)
async def get_teacher_schedule(
    teacher_id: int,
    dt_from: Annotated[Optional[datetime], Query(description="Start datetime")] = None,
    dt_to: Annotated[Optional[datetime], Query(description="End datetime")] = None,
) -> APIResponse[TeacherSchedule]:
    raise NotImplementedError
