from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


class SyncMixin:
    sync_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("synchronizations.id"),
        nullable=False,
    )


class LksMixin:
    lks_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)


class AbbrMixin:
    abbr: Mapped[str] = mapped_column(String, nullable=False)


class AbbrNameMixin(AbbrMixin):
    name: Mapped[str] = mapped_column(String, nullable=False)
