from typing import List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.audience import Audience
from app.models.base import Base, SyncMixin
from app.models.discipline import Discipline
from app.models.group import Group
from app.models.many_to_many import (
    schedule_pair_audience,
    schedule_pair_group,
    schedule_pair_teacher,
)
from app.models.teacher import Teacher


class SchedulePair(Base, SyncMixin):
    __tablename__ = "schedule_pairs"

    day: Mapped[str] = mapped_column(String, nullable=False)
    week: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[str] = mapped_column(String, nullable=False)
    end_time: Mapped[str] = mapped_column(String, nullable=False)
    unique_field: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    discipline_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("disciplines.id"),
        nullable=False,
    )
    discipline: Mapped[Discipline] = relationship(
        "Discipline",
        back_populates="schedule_pairs",
    )

    groups: Mapped[List[Group]] = relationship(
        "Group",
        secondary=schedule_pair_group,
        back_populates="schedule_pairs",
    )
    teachers: Mapped[List[Teacher]] = relationship(
        "Teacher",
        secondary=schedule_pair_teacher,
        back_populates="schedule_pairs",
    )
    audiences: Mapped[List[Audience]] = relationship(
        "Audience",
        secondary=schedule_pair_audience,
        back_populates="schedule_pairs",
    )
