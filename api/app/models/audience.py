from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SyncMixin
from app.models.many_to_many import schedule_pair_audience

if TYPE_CHECKING:
    from app.models.schedule_pair import SchedulePair


class Audience(Base, SyncMixin):
    __tablename__ = "audiences"

    lks_id: Mapped[Optional[UUID]] = mapped_column(Uuid, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    building: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unique_field: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    map_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    schedule_pairs: Mapped[list["SchedulePair"]] = relationship(
        "SchedulePair",
        secondary=schedule_pair_audience,
        back_populates="audiences",
    )
