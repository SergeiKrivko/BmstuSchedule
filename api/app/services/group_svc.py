from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends

from app.api.schemas.base import GroupBase
from app.api.schemas.group import GroupList
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

    async def get_groups(
        self,
        sessionmaker: ISessionMaker,
        abbr: Optional[str] = None,
        course: Optional[str] = None,
        department: Optional[str] = None,
        faculty: Optional[str] = None,
        filial: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> GroupList:
        async with sessionmaker() as session:
            groups, total = await self.group_repo.get_all(
                session,
                abbr=abbr,
                course_abbr=course,
                department_abbr=department,
                faculty_abbr=faculty,
                filial_abbr=filial,
                page=page,
                size=size,
            )

            group_schemas = [GroupBase.model_validate(group) for group in groups]

            return GroupList(
                items=group_schemas,
                total=total,
                page=page,
                size=size,
            )


@lru_cache(maxsize=1)
def group_svc() -> GroupSvc:
    return GroupSvc(group_repository=group_repo())


GroupSvcDep = Annotated[GroupSvc, Depends(group_svc)]
