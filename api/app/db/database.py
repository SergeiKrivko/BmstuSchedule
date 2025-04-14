from functools import lru_cache
from typing import Annotated, AsyncContextManager, Optional, Protocol

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.settings import db_settings

Base = declarative_base()

metadata = MetaData()


class ISessionMaker(Protocol):

    def __call__(self) -> AsyncContextManager[AsyncSession]: ...


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    settings = db_settings()

    return create_async_engine(
        settings.db_url,
        pool_size=settings.max_connections,
        max_overflow=5,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
        echo=False,
    )


@lru_cache(maxsize=1)
def get_session_maker(
    engine: Optional[AsyncEngine] = None,
) -> ISessionMaker:
    return async_sessionmaker(
        engine or get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )


SessionMakerDep = Annotated[
    ISessionMaker,
    Depends(get_session_maker),
]
