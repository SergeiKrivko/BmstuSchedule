from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.models.base import AbbrNameMixin, Base, LksMixin, SyncMixin

if TYPE_CHECKING:
    from app.models.filial import Filial


class University(Base, LksMixin, AbbrNameMixin, SyncMixin):
    __tablename__ = "universities"

    filials: Mapped[list["Filial"]] = relationship(
        "Filial",
        back_populates="university",
    )
