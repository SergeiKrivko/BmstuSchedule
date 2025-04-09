from sqlalchemy import Column, ForeignKey, Integer, Table, Uuid

from app.models.base import Base

schedule_pair_group = Table(
    "schedule_pair_group",
    Base.metadata,
    Column(
        "schedule_pair_id",
        Integer,
        ForeignKey("schedule_pairs.id"),
        primary_key=True,
    ),
    Column("group_id", Uuid, ForeignKey("groups.id"), primary_key=True),
)

schedule_pair_teacher = Table(
    "schedule_pair_teacher",
    Base.metadata,
    Column(
        "schedule_pair_id",
        Integer,
        ForeignKey("schedule_pairs.id"),
        primary_key=True,
    ),
    Column("teacher_id", Uuid, ForeignKey("teachers.id"), primary_key=True),
)

schedule_pair_audience = Table(
    "schedule_pair_audience",
    Base.metadata,
    Column(
        "schedule_pair_id",
        Integer,
        ForeignKey("schedule_pairs.id"),
        primary_key=True,
    ),
    Column("audience_id", Uuid, ForeignKey("audiences.id"), primary_key=True),
)
