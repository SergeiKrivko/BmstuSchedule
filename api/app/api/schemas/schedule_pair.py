from pydantic import BaseModel, Field

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.domain.day_of_week import DayOfWeek
from app.domain.timeslot import TimeSlot


class SchedulePair(BaseModel):
    day: DayOfWeek = Field(description="Day of week")
    time_slot: TimeSlot = Field(description="Time slot")
    groups: list[GroupBase] = Field(description="List of groups")
    disciplines: list[DisciplineBase] = Field(description="List of disciplines")
    teachers: list[TeacherBase] = Field(description="List of teachers in room")
    rooms: list[RoomBase] = Field(description="List of rooms")
