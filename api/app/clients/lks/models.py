from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class StructureNode(BaseModel):
    abbr: str
    name: str
    id: UUID = Field(alias="uuid")
    children: list["StructureNode"]
    type: Optional[str] = Field(None, alias="nodeType")


class Group(BaseModel):
    id: UUID = Field(alias="uuid")
    name: str


class Audience(BaseModel):
    id: Optional[UUID] = Field(None, alias="uuid")
    name: str
    building: Optional[str] = None
    structure_node_id: Optional[str] = Field(None, alias="department_uid")


class Teacher(BaseModel):
    id: UUID = Field(alias="uuid")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    last_name: str = Field(alias="lastName")


class Discipline(BaseModel):
    id: UUID = Field(alias="uuid")
    name: str


class Pair(BaseModel):
    groups: list[Group]
    audiences: list[Audience]
    teachers: list[Teacher]
    discipline: Discipline
    day: int
    time: int
    week: str
    start_time: str = Field(alias="startTime")
    end_time: str = Field(alias="endTime")


class Schedule(BaseModel):
    id: UUID = Field(alias="uuid")
    title: str
    data: list[Pair] = Field(alias="schedule")


class StructureResponseBody(BaseModel):
    data: StructureNode


class ScheduleResponseBody(BaseModel):
    data: Schedule
