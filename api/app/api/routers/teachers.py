from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query

from app.api.schemas.teacher import (
    TeacherListResponse,
    TeacherResponse,
    TeacherScheduleResponse,
)
from app.db.database import SessionMakerDep
from app.services.teacher_svc import TeacherSvcDep

router = APIRouter()


@router.get(
    "/teachers",
    tags=["teachers"],
    summary="Get list of teachers",
    response_model=TeacherListResponse,
)
async def get_teachers(
    sessionmaker: SessionMakerDep,
    teacher_svc: TeacherSvcDep,
    name: Annotated[
        Optional[str],
        Query(description="Filter teachers by any part of full name"),
    ] = None,
    group_id: Annotated[
        Optional[int],
        Query(description="Filter teachers by group ID"),
    ] = None,
    department: Annotated[
        Optional[str],
        Query(
            description="Filter teachers by department abbreviation",
        ),
    ] = None,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
) -> TeacherListResponse:
    teachers = await teacher_svc.get_teachers(
        sessionmaker,
        name=name,
        group_id=group_id,
        department=department,
        page=page,
        size=size,
    )
    return TeacherListResponse(data=teachers)


@router.get(
    "/teachers/{teacher_id}",
    tags=["teachers"],
    summary="Get a specific teacher by ID",
    response_model=TeacherResponse,
)
async def get_teacher(
    sessionmaker: SessionMakerDep,
    teacher_svc: TeacherSvcDep,
    teacher_id: Annotated[int, Path(description="ID of the teacher")],
) -> TeacherResponse:
    teacher = await teacher_svc.get_teacher(sessionmaker, teacher_id)
    return TeacherResponse(data=teacher)


@router.get(
    "/teachers/{teacher_id}/schedule",
    tags=["teachers"],
    summary="Get schedule for a specific teacher",
    response_model=TeacherScheduleResponse,
)
async def get_teacher_schedule(
    teacher_id: Annotated[int, Path(description="ID of the teacher")],
    dt_from: Annotated[Optional[datetime], Query(description="Start datetime")] = None,
    dt_to: Annotated[Optional[datetime], Query(description="End datetime")] = None,
) -> TeacherScheduleResponse:
    raise NotImplementedError
