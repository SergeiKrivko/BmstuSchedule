from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AbbrMixin, Base, LksMixin, SyncMixin
from app.models.course import Course
from app.models.many_to_many import schedule_pair_group

if TYPE_CHECKING:
    from app.models.schedule_pair import SchedulePair


class Group(Base, LksMixin, AbbrMixin, SyncMixin):
    __tablename__ = "groups"

    course_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("courses.id"),
        nullable=True,
    )
    semester_num: Mapped[int] = mapped_column(Integer, nullable=False)

    course: Mapped[Optional["Course"]] = relationship("Course", back_populates="groups")

    schedule_pairs: Mapped[list["SchedulePair"]] = relationship(
        "SchedulePair",
        secondary=schedule_pair_group,
        back_populates="groups",
    )
