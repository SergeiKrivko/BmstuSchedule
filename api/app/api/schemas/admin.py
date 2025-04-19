from pydantic import BaseModel


class SyncAPIResponse(BaseModel):
    data: None = None
