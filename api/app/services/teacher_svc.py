from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends

from app.api.schemas.base import TeacherBase
from app.api.schemas.teacher import TeacherList
from app.db.database import ISessionMaker
from app.domain.errors import NotFoundError
from app.repos.teacher_repo import TeacherRepo, teacher_repo


class TeacherSvc:
    def __init__(self, teacher_repository: TeacherRepo):
        self.teacher_repository = teacher_repository

    async def get_teacher(
        self,
        sessionmaker: ISessionMaker,
        teacher_id: int,
    ) -> TeacherBase:
        async with sessionmaker() as session:
            teacher = await self.teacher_repository.get_by_id(session, teacher_id)
            if not teacher:
                msg = "Teacher not found"
                raise NotFoundError(msg)
            return TeacherBase.model_validate(teacher)

    async def get_teachers(
        self,
        sessionmaker: ISessionMaker,
        name: Optional[str] = None,
        group_id: Optional[int] = None,
        department: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> TeacherList:
        async with sessionmaker() as session:
            teachers, total = await self.teacher_repository.get_all(
                session,
                name=name,
                group_id=group_id,
                department_abbr=department,
                page=page,
                size=size,
            )

            teacher_schemas = [
                TeacherBase.model_validate(teacher) for teacher in teachers
            ]

            return TeacherList(
                items=teacher_schemas,
                total=total,
                page=page,
                size=size,
            )


@lru_cache(maxsize=1)
def teacher_svc() -> TeacherSvc:
    return TeacherSvc(teacher_repository=teacher_repo())


TeacherSvcDep = Annotated[TeacherSvc, Depends(teacher_svc)]
