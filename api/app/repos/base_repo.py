from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepo(Generic[T]):
    model: Type[T]

    async def get_by_id(self, session: AsyncSession, record_id: int) -> Optional[T]:
        return await session.get(self.model, record_id)

    async def add(self, session: AsyncSession, record: T) -> T:
        session.add(record)
        await session.flush()
        await session.refresh(record)
        return record


class LksIdRepo(BaseRepo[T]):
    async def get_by_lks_id(
        self,
        session: AsyncSession,
        lks_id: UUID,
    ) -> Optional[T]:
        res = await session.execute(
            select(self.model).where(self.model.lks_id == lks_id),
        )
        return res.scalar_one_or_none()


class UniqueFieldRepo(BaseRepo[T]):
    async def get_by_unique_field(
        self,
        session: AsyncSession,
        unique_field: str,
    ) -> Optional[T]:
        res = await session.execute(
            select(self.model).where(self.model.unique_field == unique_field),
        )
        return res.scalar_one_or_none()
