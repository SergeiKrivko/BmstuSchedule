from datetime import datetime
from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends

from app.api.schemas.base import RoomBase
from app.api.schemas.room import RoomList, RoomSchedule
from app.core.schedule_manager import ScheduleManager, schedule_manager
from app.db.database import ISessionMaker
from app.domain.errors import NotFoundError
from app.repos.audience_repo import AudienceRepo, audience_repo
from app.services.schedule_mixin import ScheduleMixin


class RoomSvc(ScheduleMixin):
    def __init__(
        self,
        audience_repository: AudienceRepo,
        schedule_manager: ScheduleManager,
    ) -> None:
        super().__init__(schedule_manager)
        self.audience_repo = audience_repository

    async def get_room(
        self,
        sessionmaker: ISessionMaker,
        room_id: int,
    ) -> RoomBase:
        async with sessionmaker() as session:
            room = await self.audience_repo.get_by_id(session, room_id)
            if not room:
                msg = "Room not found"
                raise NotFoundError(msg)
        return RoomBase(
            id=room.id,
            name=room.name,
            building=room.building,
            map_url=room.map_url,
        )

    async def get_rooms(
        self,
        sessionmaker: ISessionMaker,
        building: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> RoomList:
        async with sessionmaker() as session:
            rooms, total = await self.audience_repo.get_all(
                session,
                building=building,
                page=page,
                size=size,
            )

            room_schemas = [
                RoomBase(
                    id=room.id,
                    name=room.name,
                    building=room.building,
                    map_url=room.map_url,
                )
                for room in rooms
            ]
            return RoomList(
                items=room_schemas,
                total=total,
                page=page,
                size=size,
            )

    async def get_room_schedule(
        self,
        sessionmaker: ISessionMaker,
        room_id: int,
        dt_from: datetime,
        dt_to: datetime,
    ) -> RoomSchedule:
        async with sessionmaker() as session:
            schedule_result = await self.audience_repo.get_schedule_by_audience_id(
                session=session,
                audience_id=room_id,
            )
            if not schedule_result:
                msg = "Room schedule not found"
                raise NotFoundError(msg)

            concrete_pairs = await self._generate_concrete_pairs(
                schedule_result=schedule_result,
                dt_from=dt_from,
                dt_to=dt_to,
            )

            return RoomSchedule(
                room=RoomBase(
                    id=schedule_result.entity.id,
                    name=schedule_result.entity.name,
                    building=schedule_result.entity.building,
                    map_url=schedule_result.entity.map_url,
                ),
                schedule=concrete_pairs,
            )


@lru_cache
def room_svc() -> RoomSvc:
    return RoomSvc(
        audience_repository=audience_repo(),
        schedule_manager=schedule_manager(),
    )


RoomSvcDep = Annotated[RoomSvc, Depends(room_svc)]
