from functools import lru_cache
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.schedule_pair import SchedulePair
from app.repos.base_repo import UniqueFieldRepo


class SchedulePairRepo(UniqueFieldRepo[SchedulePair]):
    model = SchedulePair

    async def get_by_unique_field(
        self,
        session: AsyncSession,
        unique_field: str,
    ) -> Optional[SchedulePair]:
        res = await session.execute(
            select(self.model)
            .where(self.model.unique_field == unique_field)
            .options(
                joinedload(SchedulePair.groups),
            ),
        )
        return res.scalar_one_or_none()


@lru_cache(maxsize=1)
def schedule_pair_repo() -> SchedulePairRepo:
    return SchedulePairRepo()
