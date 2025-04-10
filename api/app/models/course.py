from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AbbrMixin, Base, LksMixin, SyncMixin
from app.models.department import Department

if TYPE_CHECKING:
    from app.models.group import Group


class Course(Base, LksMixin, AbbrMixin, SyncMixin):
    __tablename__ = "courses"

    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False,
    )
    course_num: Mapped[int] = mapped_column(Integer, nullable=False)

    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="courses",
    )
    groups: Mapped[list["Group"]] = relationship("Group", back_populates="course")
