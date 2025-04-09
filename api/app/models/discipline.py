import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SyncMixin

if TYPE_CHECKING:
    from app.models.schedule_pair import SchedulePair


class Discipline(Base, SyncMixin):
    __tablename__ = "disciplines"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)

    schedule_pairs: Mapped[list["SchedulePair"]] = relationship(
        "SchedulePair",
        back_populates="discipline",
    )
