from datetime import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import now


class Base(DeclarativeBase):
    pass


class SyncMixin:
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=now(),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
