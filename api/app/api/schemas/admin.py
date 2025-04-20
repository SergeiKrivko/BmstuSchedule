from app.api.schemas.response import APIResponse


class SyncAPIResponse(APIResponse):
    data: None = None


class PostMigrationsUpgradeAPIResponse(APIResponse):
    data: str
    detail: str = "Migration upgrade successful."
