from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class TeacherBase(BaseModel):
    id: int = Field(description="Teacher ID")
    first_name: str = Field(description="Teacher first name", examples=["Наталья"])
    middle_name: str = Field(description="Teacher middle name", examples=["Юрьевна"])
    last_name: str = Field(description="Teacher last name", examples=["Рязанова"])

    departments: list[str] = Field(
        description="List of department abbreviations where teacher works",
        examples=["ИУ7"],
    )


class RoomBase(BaseModel):
    id: int = Field(description="Room ID")
    name: str = Field(description="Room name", examples=["91"])
    building: Optional[str] = Field(
        None,
        description="Building name",
        examples=["Химлаб"],
    )
    map_url: Optional[HttpUrl] = Field(
        None,
        description="URL with room in query params of interactive map",
        examples=["https://map.mf.bmstu.ru/?location=room-91"],
    )


class DisciplineBase(BaseModel):
    id: int = Field(description="Discipline ID")
    abbr: str = Field(description="Discipline abbreviation", examples=["ИиДУ"])
    full_name: str = Field(
        description="Discipline full name",
        examples=["Интегралы и дифференциальные уравнения"],
    )
    short_name: str = Field(
        description="Discipline short name",
        examples=["Интегр. и дифф. уравнения"],
    )
    act_type: Optional[str] = Field(
        None,
        description="Discipline act type",
        examples=["seminar"],
    )


class GroupBase(BaseModel):
    id: int = Field(description="Group ID")
    abbr: str = Field(description="Group abbreviation")
    course_id: int = Field(description="Course ID")
    semester_num: int = Field(description="Semester number")

    model_config = ConfigDict(from_attributes=True)
