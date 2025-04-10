from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AbbrMixin, Base, LksMixin, SyncMixin

if TYPE_CHECKING:
    from app.models.schedule_pair import SchedulePair


class Discipline(Base, LksMixin, AbbrMixin, SyncMixin):
    __tablename__ = "disciplines"

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    short_name: Mapped[str] = mapped_column(String, nullable=False)
    act_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    schedule_pairs: Mapped[list["SchedulePair"]] = relationship(
        "SchedulePair",
        back_populates="discipline",
    )
