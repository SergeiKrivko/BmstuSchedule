import subprocess

from fastapi import APIRouter, BackgroundTasks
from loguru import logger

from app.api.schemas.admin import PostMigrationsUpgradeAPIResponse, SyncAPIResponse
from app.db.database import SessionMakerDep
from app.services.sync_svc import SyncSvcDep

router = APIRouter()


@router.post(
    "/admin/sync",
    tags=["admin"],
    summary="Sync data from LKS",
    response_model=SyncAPIResponse,
)
async def sync_data(
    sessionmaker: SessionMakerDep,
    sync_svc: SyncSvcDep,
    bt: BackgroundTasks,
) -> SyncAPIResponse:
    await sync_svc.add_synchronization_task(sessionmaker, bt)
    return SyncAPIResponse()


@router.post(
    "/admin/migrations/upgrade",
    tags=["admin"],
    summary="Database migration upgrade",
    description=(
        "Накатывает миграции вплоть до head ревизии "
        "на PostgreSQL с помощью alembic. "
    ),
    response_model=PostMigrationsUpgradeAPIResponse,
)
async def post_migrations_upgrade() -> PostMigrationsUpgradeAPIResponse:
    alembic_output = subprocess.check_output(  # noqa: S603
        ["poetry", "run", "alembic", "upgrade", "head"],  # noqa: S607
        text=True,
        stderr=subprocess.STDOUT,
    )

    logger.info(f"Migration upgrade successful: {alembic_output}.")
    return PostMigrationsUpgradeAPIResponse(data=alembic_output)
