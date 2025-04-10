from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, LksMixin, SyncMixin
from app.models.many_to_many import schedule_pair_audience

if TYPE_CHECKING:
    from app.models.schedule_pair import SchedulePair


class Audience(Base, LksMixin, SyncMixin):
    __tablename__ = "audiences"

    name: Mapped[str] = mapped_column(String, nullable=False)
    building: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    map_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    schedule_pairs: Mapped[list["SchedulePair"]] = relationship(
        "SchedulePair",
        secondary=schedule_pair_audience,
        back_populates="audiences",
    )
