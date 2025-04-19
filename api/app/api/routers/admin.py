from fastapi import APIRouter

from app.api.schemas.admin import SyncAPIResponse

router = APIRouter()


@router.post("/admin/sync", response_model=SyncAPIResponse)
async def sync_data() -> SyncAPIResponse:
    raise NotImplementedError
