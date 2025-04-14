from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.api.schemas.base import GroupBase
from app.db.database import ISessionMaker
from app.domain.errors import NotFoundError
from app.repos.group_repo import GroupRepo, group_repo


class GroupSvc:
    def __init__(self, group_repository: GroupRepo):
        self.group_repo = group_repository

    async def get_group(
        self,
        sessionmaker: ISessionMaker,
        group_id: int,
    ) -> GroupBase:
        async with sessionmaker() as session:
            group = await self.group_repo.get_by_id(session, group_id)
            if not group:
                msg = "Group not found"
                raise NotFoundError(msg)
        return GroupBase.model_validate(group)


@lru_cache(maxsize=1)
def group_svc() -> GroupSvc:
    return GroupSvc(group_repository=group_repo())


GroupSvcDep = Annotated[GroupSvc, Depends(group_svc)]
