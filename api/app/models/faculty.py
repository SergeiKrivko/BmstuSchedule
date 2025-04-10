from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AbbrNameMixin, Base, LksMixin, SyncMixin
from app.models.filial import Filial

if TYPE_CHECKING:
    from app.models.department import Department


class Faculty(Base, LksMixin, AbbrNameMixin, SyncMixin):
    __tablename__ = "faculties"

    filial_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("filials.id"),
        nullable=False,
    )

    filial: Mapped["Filial"] = relationship("Filial", back_populates="faculties")
    departments: Mapped[list["Department"]] = relationship(
        "Department",
        back_populates="faculty",
    )
