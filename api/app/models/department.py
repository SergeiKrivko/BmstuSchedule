from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AbbrNameMixin, Base, LksMixin, SyncMixin
from app.models.faculty import Faculty

if TYPE_CHECKING:
    from app.models.course import Course


class Department(Base, LksMixin, AbbrNameMixin, SyncMixin):
    __tablename__ = "departments"

    faculty_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("faculties.id"),
        nullable=False,
    )

    faculty: Mapped["Faculty"] = relationship("Faculty", back_populates="departments")
    courses: Mapped[list["Course"]] = relationship(
        "Course",
        back_populates="department",
    )
