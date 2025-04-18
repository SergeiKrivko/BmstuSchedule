from datetime import datetime
from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends

from app.api.schemas.base import GroupBase
from app.api.schemas.group import (
    GroupList,
    GroupSchedule,
)
from app.api.schemas.schedule_pair import SchedulePairRead
from app.db.database import ISessionMaker
from app.domain.errors import NotFoundError
from app.domain.timeslot import TimeSlot
from app.repos.group_repo import GroupRepo, group_repo


class GroupSvc:
    def __init__(self, group_repository: GroupRepo):
        self.group_repo = group_repository

    async def get_group(
        self,
        sessionmaker: ISessionMaker,
        group_id: int,
    ) -> GroupBase:
        async with sessionmaker() as session:
            group = await self.group_repo.get_by_id(session, group_id)
            if not group:
                msg = "Group not found"
                raise NotFoundError(msg)
        return GroupBase.model_validate(group)

    async def get_groups(
        self,
        sessionmaker: ISessionMaker,
        abbr: Optional[str] = None,
        course: Optional[str] = None,
        department: Optional[str] = None,
        faculty: Optional[str] = None,
        filial: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> GroupList:
        async with sessionmaker() as session:
            groups, total = await self.group_repo.get_all(
                session,
                abbr=abbr,
                course_abbr=course,
                department_abbr=department,
                faculty_abbr=faculty,
                filial_abbr=filial,
                page=page,
                size=size,
            )

            group_schemas = [GroupBase.model_validate(group) for group in groups]

            return GroupList(
                items=group_schemas,
                total=total,
                page=page,
                size=size,
            )

    async def get_group_schedule(
        self,
        sessionmaker: ISessionMaker,
        group_id: int,
        dt_from: datetime,
        dt_to: datetime,
    ) -> GroupSchedule:
        async with sessionmaker() as session:
            schedule_result = await self.group_repo.get_schedule_by_group_id(
                session,
                group_id,
                dt_from=dt_from,
                dt_to=dt_to,
            )

            if not schedule_result:
                msg = "Group schedule not found"
                raise NotFoundError(msg)

            schedule_items = []
            for concrete_pair in schedule_result.schedule_pairs:
                schedule_item = SchedulePairRead(
                    time_slot=TimeSlot(
                        start_time=concrete_pair.time_slot.start_time,
                        end_time=concrete_pair.time_slot.end_time,
                    ),
                    teachers=concrete_pair.teachers,
                    disciplines=concrete_pair.disciplines,
                    rooms=concrete_pair.audiences,  # переименовываем audiences в rooms
                    groups=concrete_pair.groups,
                )
                schedule_items.append(schedule_item)

            return GroupSchedule(
                group=schedule_result.group,
                schedule=schedule_items,
            )


@lru_cache(maxsize=1)
def group_svc() -> GroupSvc:
    return GroupSvc(group_repository=group_repo())


GroupSvcDep = Annotated[GroupSvc, Depends(group_svc)]
