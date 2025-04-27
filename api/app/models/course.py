from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AbbrMixin, Base, SyncMixin
from app.models.department import Department

if TYPE_CHECKING:
    from app.models.group import Group


class Course(Base, AbbrMixin, SyncMixin):
    __tablename__ = "courses"

    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False,
    )
    course_num: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_field: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="courses",
    )
    groups: Mapped[list["Group"]] = relationship("Group", back_populates="course")
