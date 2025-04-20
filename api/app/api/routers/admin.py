import subprocess
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Path

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
    await sync_svc.sync_data(sessionmaker, bt)
    return SyncAPIResponse()


@router.post(
    "/admin/migrations/{name}/upgrade",
    tags=["admin"],
    summary="Database migration upgrade",
    description="Накатывает миграции вплоть до указанной ревизии на PostgreSQL с помощью alembic. Ожидается, что в основном ручка будет вызываться с `name=head`",
    response_model=PostMigrationsUpgradeAPIResponse,
)
async def post_migrations_upgrade(
    name: Annotated[str, Path(description="Название ревизии", example="head")],
) -> PostMigrationsUpgradeAPIResponse:
    try:
        alembic_output = subprocess.check_output(
            ["poetry", "run", "alembic", "upgrade", name],
            text=True,
            stderr=subprocess.STDOUT,
        )

        print(f"Migration upgrade successful: {alembic_output}.")
        return PostMigrationsUpgradeAPIResponse(data=alembic_output)
    except Exception as e:
        err = "Failed to upgrade migrations"
        print(f"{err}: {e}.")
        raise RuntimeError(err)
