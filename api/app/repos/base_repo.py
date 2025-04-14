from typing import Generic, Optional, Type, TypeVar

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
