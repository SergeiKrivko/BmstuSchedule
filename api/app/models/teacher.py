from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, LksMixin, SyncMixin
from app.models.many_to_many import schedule_pair_teacher

if TYPE_CHECKING:
    from app.models.schedule_pair import SchedulePair


class Teacher(Base, LksMixin, SyncMixin):
    __tablename__ = "teachers"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    schedule_pairs: Mapped[list["SchedulePair"]] = relationship(
        "SchedulePair",
        secondary=schedule_pair_teacher,
        back_populates="teachers",
    )
