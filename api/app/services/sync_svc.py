from functools import lru_cache
from typing import Annotated

from fastapi import BackgroundTasks, Depends
from loguru import logger

from app.db.database import ISessionMaker
from app.domain.sync_status import SyncStatus
from app.models.synchronization import Synchronization
from app.repos.sync_repo import SyncRepo, sync_repo
from app.utils.lks_synchronizer import LksSynchronizer, lks_synchronizer


class SyncSvc:
    def __init__(self, sync_repository: SyncRepo, lks_syncer: LksSynchronizer):
        self.sync_repo = sync_repository
        self.lks_synchronizer = lks_syncer

    async def add_synchronization_task(
        self,
        sessionmaker: ISessionMaker,
        bt: BackgroundTasks,
    ) -> None:
        async with sessionmaker() as session:
            sync_model = Synchronization(
                status=SyncStatus.IN_PROGRESS,
            )
            await self.sync_repo.add(session, sync_model)
            await session.commit()
            logger.info(f"Syncing task added (sync_id: {sync_model.id})")

        bt.add_task(self._synchronize, sessionmaker, sync_model.id)

    async def _synchronize(self, sessionmaker: ISessionMaker, sync_id: int) -> None:
        try:
            logger.info(f"Syncing with LKS (sync_id: {sync_id})")
            await self.lks_synchronizer.synchronize(sessionmaker, sync_id)
            status = SyncStatus.SUCCESS
        except Exception as e:  # noqa: BLE001
            logger.error(
                f"Error syncing with LKS (sync_id: {sync_id}): {e}",
            )
            status = SyncStatus.FAILED

        async with sessionmaker() as session:
            await self.sync_repo.update_status(session, sync_id, status)
            await session.commit()

        logger.success(f"Syncing with LKS (sync_id: {sync_id}) completed")


@lru_cache(maxsize=1)
def sync_svc() -> SyncSvc:
    return SyncSvc(
        sync_repository=sync_repo(),
        lks_syncer=lks_synchronizer(),
    )


SyncSvcDep = Annotated[SyncSvc, Depends(sync_svc)]
