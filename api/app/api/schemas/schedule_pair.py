from pydantic import BaseModel, Field

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.domain.timeslot import TimeSlot


class SchedulePairRead(BaseModel):
    id: int = Field(description="ID of the schedule pair")
    time_slot: TimeSlot = Field(description="Time slot")
    groups: list[GroupBase] = Field(description="List of groups")
    disciplines: list[DisciplineBase] = Field(description="List of disciplines")
    teachers: list[TeacherBase] = Field(description="List of teachers in room")
    rooms: list[RoomBase] = Field(description="List of rooms")
