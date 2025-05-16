from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from app.models.base import Base
from app.models.schedule_pair import SchedulePair

T = TypeVar("T", bound=Base)


class ScheduleResult(BaseModel, Generic[T]):
    entity: T
    pairs: list[SchedulePair]

    model_config = ConfigDict(arbitrary_types_allowed=True)
