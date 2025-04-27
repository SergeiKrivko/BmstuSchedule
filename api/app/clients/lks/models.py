from enum import IntEnum, StrEnum
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class StructureNodeType(StrEnum):
    DEPARTMENT = "department"
    GROUP = "group"
    FACULTY = "faculty"
    FILIAL = "filial"
    COURSE = "course"
    UNIVERSITY = "university"


class StructureNode(BaseModel):
    abbr: Optional[str] = None
    name: Optional[str] = None
    id: Annotated[Optional[UUID], Field(alias="uuid")] = None
    children: Annotated[list["StructureNode"], Field(default_factory=list)] = Field(
        default_factory=list,
    )
    type: Optional[StructureNodeType] = Field(None, alias="nodeType")
    department_id: Annotated[Optional[UUID], Field(alias="parentUuid")] = None
    semester_num: Annotated[Optional[int], Field(alias="semester")] = None


class Group(BaseModel):
    id: UUID = Field(alias="uuid")
    name: str


class Audience(BaseModel):
    id: Optional[UUID] = Field(None, alias="uuid")
    name: str
    building: Optional[str] = None
    department_id: Optional[UUID] = Field(None, alias="department_uid")


class Teacher(BaseModel):
    id: UUID = Field(alias="uuid")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    last_name: str = Field(alias="lastName")


class Discipline(BaseModel):
    id: Optional[UUID] = Field(None, alias="uuid")
    abbr: str
    act_type: Optional[str] = Field(None, alias="actType")
    full_name: str = Field(alias="fullName")
    short_name: str = Field(alias="shortName")


class Week(StrEnum):
    ALL = "all"
    ODD = "ch"
    EVEN = "zn"


class Day(IntEnum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7


class SchedulePair(BaseModel):
    groups: list[Group]
    audiences: list[Audience]
    teachers: list[Teacher]
    discipline: Discipline
    day: Day
    week: Week
    start_time: str = Field(alias="startTime")
    end_time: str = Field(alias="endTime")


class Schedule(BaseModel):
    id: UUID = Field(alias="uuid")
    title: str
    data: list[SchedulePair] = Field(alias="schedule")


class StructureResponseBody(BaseModel):
    data: StructureNode


class ScheduleResponseBody(BaseModel):
    data: Schedule
