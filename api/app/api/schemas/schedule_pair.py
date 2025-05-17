from pydantic import BaseModel, Field

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.domain.timeslot import TimeSlot


class SchedulePairRead(BaseModel):
    time_slot: TimeSlot = Field(description="Time slot")
    groups: list[GroupBase] = Field(description="List of groups")
    discipline: DisciplineBase = Field(description="Discipline")
    teachers: list[TeacherBase] = Field(description="List of teachers in room")
    rooms: list[RoomBase] = Field(description="List of rooms")
