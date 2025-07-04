from functools import lru_cache
from typing import Optional, Sequence, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import count

from app.domain.schedule import ScheduleResult
from app.models.course import Course
from app.models.group import Group
from app.models.many_to_many import schedule_pair_group
from app.models.schedule_pair import SchedulePair
from app.repos.base_repo import LksIdRepo


class GroupRepo(LksIdRepo[Group]):
    model = Group

    async def get_all(
        self,
        session: AsyncSession,
        abbr: Optional[str] = None,
        course_abbr: Optional[str] = None,
        department_abbr: Optional[str] = None,
        faculty_abbr: Optional[str] = None,
        filial_abbr: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> Tuple[Sequence[Group], int]:
        query = select(self.model)

        if abbr:
            query = query.where(self.model.abbr.ilike(f"%{abbr}%"))

        if course_abbr:
            query = query.join(self.model.course).where(
                Course.abbr.ilike(f"%{course_abbr}%"),
            )

        # todo other joins
        if department_abbr or faculty_abbr or filial_abbr:
            msg = "Department, faculty and filial filters are not implemented"
            raise NotImplementedError(msg)

        count_query = select(count()).select_from(query.subquery())
        total = await session.scalar(count_query)

        query = query.order_by(self.model.created_at.desc())
        if page is not None and size is not None:
            query = query.offset((page - 1) * size).limit(size)

        result = await session.execute(query)
        groups = result.scalars().all()

        return groups, total or 0

    async def get_schedule_by_group_id(
        self,
        session: AsyncSession,
        group_id: int,
    ) -> Optional[ScheduleResult[Group]]:
        group_query = select(self.model).where(self.model.id == group_id)
        group_result = await session.execute(group_query)
        group = group_result.scalars().first()

        if not group:
            return None

        pairs_query = (
            select(SchedulePair)
            .options(
                joinedload(SchedulePair.teachers),
                joinedload(SchedulePair.audiences),
                joinedload(SchedulePair.discipline),
                joinedload(SchedulePair.groups),
            )
            .join(
                schedule_pair_group,
                SchedulePair.id == schedule_pair_group.c.schedule_pair_id,
            )
            .where(
                schedule_pair_group.c.group_id == group_id,
            )
        )

        result = await session.execute(pairs_query)
        schedule_pairs = result.unique().scalars().all()

        return ScheduleResult[Group](entity=group, pairs=schedule_pairs)


@lru_cache(maxsize=1)
def group_repo() -> GroupRepo:
    return GroupRepo()
