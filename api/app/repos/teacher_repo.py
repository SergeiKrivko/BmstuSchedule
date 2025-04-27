from functools import lru_cache
from typing import Optional, Sequence

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from app.models.group import Group
from app.models.schedule_pair import SchedulePair
from app.models.teacher import Teacher
from app.repos.base_repo import LksIdRepo


class TeacherRepo(LksIdRepo[Teacher]):
    model = Teacher

    async def get_all(
        self,
        session: AsyncSession,
        name: Optional[str] = None,
        group_id: Optional[int] = None,
        department_abbr: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[Sequence[Teacher], int]:
        query = select(self.model)

        if name:
            name_parts = name.split(" ")
            for name_part in name_parts:
                query = query.where(
                    or_(
                        self.model.first_name.ilike(f"%{name_part}%"),
                        self.model.middle_name.ilike(f"%{name_part}%"),
                        self.model.last_name.ilike(f"%{name_part}%"),
                    ),
                )

        if group_id:
            query = query.where(
                self.model.schedule_pairs.any(
                    SchedulePair.groups.any(
                        Group.id == group_id,
                    ),
                ),
            )

        if department_abbr:
            msg = "Department abbreviation filter is not implemented"
            raise NotImplementedError(msg)

        count_query = select(count()).select_from(query.subquery())
        total = await session.scalar(count_query)

        query = (
            query.order_by(self.model.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await session.execute(query)
        teachers = result.unique().scalars().all()

        return teachers, total or 0


@lru_cache(maxsize=1)
def teacher_repo() -> TeacherRepo:
    return TeacherRepo()
