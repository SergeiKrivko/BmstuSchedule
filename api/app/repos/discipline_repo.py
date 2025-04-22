from functools import lru_cache
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.discipline import Discipline
from app.repos.base_repo import BaseRepo


class DisciplineRepo(BaseRepo[Discipline]):
    model = Discipline

    async def get_by_abbr(
        self,
        session: AsyncSession,
        abbr: str,
    ) -> Optional[Discipline]:
        result = await session.execute(
            select(Discipline).where(Discipline.abbr == abbr),
        )
        return result.scalar_one_or_none()


@lru_cache(maxsize=1)
def discipline_repo() -> DisciplineRepo:
    return DisciplineRepo()
