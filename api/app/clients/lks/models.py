from uuid import UUID

from pydantic import BaseModel, Field


class Node(BaseModel):
    abbr: str
    name: str
    id: UUID = Field(alias="uuid")
    children: list["Node"]
    type: str = Field(alias="nodeType")


class Group(BaseModel):
    id: UUID = Field(alias="uuid")
    name: str


class Audience(BaseModel):
    id: UUID = Field(alias="uuid")
    name: str


class Teacher(BaseModel):
    id: UUID = Field(alias="uuid")
    name: str


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
    data: Node


class ScheduleResponseBody(BaseModel):
    data: Schedule
