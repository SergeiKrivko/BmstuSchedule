import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SyncMixin


class StructureNode(Base, SyncMixin):
    __tablename__ = "structure_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lks_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    abbr: Mapped[str] = mapped_column(String, nullable=False)
    node_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("structure_nodes.id"),
        nullable=True,
    )
    children: Mapped[list["StructureNode"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    parent: Mapped[Optional["StructureNode"]] = relationship(
        back_populates="children",
        remote_side="StructureNode.id",
    )
