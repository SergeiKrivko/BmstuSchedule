from functools import lru_cache
from typing import Optional, Sequence, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from app.models.course import Course
from app.models.group import Group
from app.repos.base_repo import BaseRepo


class GroupRepo(BaseRepo[Group]):
    model = Group

    async def get_all(
        self,
        session: AsyncSession,
        abbr: Optional[str] = None,
        course_abbr: Optional[str] = None,
        department_abbr: Optional[str] = None,
        faculty_abbr: Optional[str] = None,
        filial_abbr: Optional[str] = None,
        page: int = 1,
        size: int = 20,
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

        query = (
            query.order_by(self.model.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await session.execute(query)
        groups = result.scalars().all()

        return groups, total or 0


@lru_cache(maxsize=1)
def group_repo() -> GroupRepo:
    return GroupRepo()
