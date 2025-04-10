from app.models.audience import Audience
from app.models.base import AbbrMixin, AbbrNameMixin, Base, LksMixin, SyncMixin
from app.models.course import Course
from app.models.department import Department
from app.models.discipline import Discipline
from app.models.faculty import Faculty
from app.models.filial import Filial
from app.models.group import Group
from app.models.many_to_many import (
    schedule_pair_audience,
    schedule_pair_group,
    schedule_pair_teacher,
)
from app.models.schedule_pair import SchedulePair
from app.models.sync import Sync
from app.models.teacher import Teacher

__all__ = [
    "AbbrMixin",
    "AbbrNameMixin",
    "Audience",
    "Base",
    "Course",
    "Department",
    "Discipline",
    "Faculty",
    "Filial",
    "Group",
    "LksMixin",
    "SchedulePair",
    "Sync",
    "SyncMixin",
    "Teacher",
    "schedule_pair_audience",
    "schedule_pair_group",
    "schedule_pair_teacher",
]
