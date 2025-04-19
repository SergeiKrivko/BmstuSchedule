from pydantic import BaseModel

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.domain.timeslot import TimeSlot


class ConcreteSchedulePair(BaseModel):
    id: int
    time_slot: TimeSlot
    disciplines: list[DisciplineBase]
    teachers: list[TeacherBase]
    audiences: list[RoomBase]
    groups: list[GroupBase]


class GroupScheduleResult(BaseModel):
    group: GroupBase
    schedule_pairs: list[ConcreteSchedulePair]
