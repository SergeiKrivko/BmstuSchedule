from typing import List

from pydantic import BaseModel

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.domain.timeslot import TimeSlot


class ConcreteSchedulePair(BaseModel):
    id: int
    time_slot: TimeSlot
    discipline: DisciplineBase
    teachers: List[TeacherBase]
    audiences: List[RoomBase]


class GroupScheduleResult(BaseModel):
    group: GroupBase
    schedule_pairs: List[ConcreteSchedulePair]
