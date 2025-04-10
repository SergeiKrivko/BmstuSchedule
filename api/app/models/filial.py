from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AbbrNameMixin, Base, LksMixin, SyncMixin
from app.models.university import University

if TYPE_CHECKING:
    from app.models.faculty import Faculty


class Filial(Base, LksMixin, AbbrNameMixin, SyncMixin):
    __tablename__ = "filials"

    university_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("universities.id"),
        nullable=False,
    )

    university: Mapped["University"] = relationship(
        "University",
        back_populates="filials",
    )
    faculties: Mapped[list["Faculty"]] = relationship(
        "Faculty",
        back_populates="filial",
    )
