from functools import lru_cache
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import count

from app.domain.schedule import ScheduleResult
from app.models.audience import Audience
from app.models.many_to_many import schedule_pair_audience
from app.models.schedule_pair import SchedulePair
from app.repos.base_repo import UniqueFieldRepo


class AudienceRepo(UniqueFieldRepo[Audience]):
    model = Audience

    async def get_all(
        self,
        session: AsyncSession,
        building: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> tuple[Sequence[Audience], int]:
        query = select(self.model)

        if building:
            query = query.where(self.model.building.ilike(f"%{building}%"))

        count_query = select(count()).select_from(query.subquery())
        total = await session.scalar(count_query)

        query = query.order_by(self.model.created_at.desc())
        if page and size:
            query = query.offset((page - 1) * size).limit(size)

        result = await session.execute(query)
        audiences = result.scalars().all()

        return audiences, total or 0

    async def get_schedule_by_audience_id(
        self,
        session: AsyncSession,
        audience_id: int,
    ) -> Optional[ScheduleResult[Audience]]:
        audience_query = select(self.model).where(self.model.id == audience_id)
        audience_result = await session.execute(audience_query)
        audience = audience_result.scalars().first()

        if not audience:
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
                schedule_pair_audience,
                SchedulePair.id == schedule_pair_audience.c.schedule_pair_id,
            )
            .where(
                schedule_pair_audience.c.audience_id == audience_id,
            )
        )

        result = await session.execute(pairs_query)
        schedule_pairs = result.unique().scalars().all()

        return ScheduleResult[Audience](entity=audience, pairs=schedule_pairs)


@lru_cache(maxsize=1)
def audience_repo() -> AudienceRepo:
    return AudienceRepo()
