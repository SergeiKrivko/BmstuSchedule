from pydantic import BaseModel


class Student(BaseModel):
    full_name: str
    id: str
    group_alias: str
