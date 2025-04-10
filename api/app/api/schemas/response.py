from pydantic import BaseModel


class APIResponse(BaseModel):
    detail: str = "Operation completed successfully"
