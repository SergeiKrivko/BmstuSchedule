from functools import lru_cache

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sync_status import SyncStatus
from app.models.synchronization import Synchronization
from app.repos.base_repo import BaseRepo


class SyncRepo(BaseRepo[Synchronization]):
    model = Synchronization

    async def update_status(
        self,
        session: AsyncSession,
        sync_id: int,
        status: SyncStatus,
    ) -> None:
        await session.execute(
            update(self.model).where(self.model.id == sync_id).values(status=status),
        )


@lru_cache(maxsize=1)
def sync_repo() -> SyncRepo:
    return SyncRepo()
