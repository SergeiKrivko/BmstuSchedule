from enum import StrEnum
from functools import lru_cache

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.lks.client import LksClient, lks_client
from app.clients.lks.models import StructureNode, StructureNodeType
from app.db.database import ISessionMaker
from app.models.course import Course
from app.models.department import Department
from app.models.faculty import Faculty
from app.models.filial import Filial
from app.models.group import Group
from app.models.synchronization import Synchronization
from app.models.university import University
from app.repos.course_repo import CourseRepo, course_repo
from app.repos.department_repo import DepartmentRepo, department_repo
from app.repos.faculty_repo import FacultyRepo, faculty_repo
from app.repos.filial_repo import FilialRepo, filial_repo
from app.repos.group_repo import GroupRepo, group_repo
from app.repos.sync_repo import SyncRepo, sync_repo
from app.repos.university_repo import UniversityRepo, university_repo


class SyncStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"


class LksSynchronizer:
    def __init__(
        self,
        lks_api_client: LksClient,
        sync_repository: SyncRepo,
        group_repository: GroupRepo,
        course_repository: CourseRepo,
        department_repository: DepartmentRepo,
        faculty_repository: FacultyRepo,
        filial_repository: FilialRepo,
        university_repository: UniversityRepo,
    ) -> None:
        self.lks_client = lks_api_client
        self.sync_repository = sync_repository
        self.group_repository = group_repository
        self.course_repository = course_repository
        self.department_repository = department_repository
        self.faculty_repository = faculty_repository
        self.filial_repository = filial_repository
        self.university_repository = university_repository

    async def sync_structure(self, sessionmaker: ISessionMaker, sync_id: int) -> None:
        pass

    async def sync_group(
        self,
        session: AsyncSession,
        structure: StructureNode,
        sync_id: int,
    ) -> Group:
        course_lks_id = structure.course_id  # parentUuid в lks есть для групп
        course = await self.course_repository.get_by_lks_id(session, course_lks_id)
        if not course:
            raise ValueError(f"Course with lks_id {course_lks_id} not found")

        group = Group(
            sync_id=sync_id,
            lks_id=structure.id,
            abbr=structure.abbr,
            course_id=course.id,
        )
        await self.group_repository.add(session, group)
        return group

    async def sync_department(
        self,
        session: AsyncSession,
        structure: StructureNode,
        sync_id: int,
    ) -> Department:
        pass

    async def sync_faculty(
        self,
        session: AsyncSession,
        structure: StructureNode,
        sync_id: int,
    ) -> Faculty:
        pass

    async def sync_filial(
        self,
        session: AsyncSession,
        structure: StructureNode,
        sync_id: int,
    ) -> Filial:
        pass

    async def sync_course(
        self,
        session: AsyncSession,
        structure: StructureNode,
        sync_id: int,
    ) -> Course:
        pass

    async def sync_university(
        self,
        session: AsyncSession,
        structure: StructureNode,
        sync_id: int,
    ) -> University:
        u = await self.university_repository.get_by_lks_id(session, structure.id)
        if not u:
            u = University(
                lks_id=structure.id,
                abbr=structure.abbr,
                name=structure.name,
            )

        u.sync_id = sync_id
        await self.university_repository.add(session, u)
        return u


@lru_cache(maxsize=1)
def lks_synchronizer() -> LksSynchronizer:
    return LksSynchronizer(
        lks_client=lks_client(),
        sync_repository=sync_repo(),
        group_repository=group_repo(),
        course_repository=course_repo(),
        department_repository=department_repo(),
        faculty_repository=faculty_repo(),
        filial_repository=filial_repo(),
        university_repository=university_repo(),
    )


class SyncSvc:
    def __init__(self, sync_repo: SyncRepo, lks_syncer: LksSynchronizer):
        self.sync_repo = sync_repo
        self.lks_synchronizer = lks_syncer

    async def sync_data(
        self,
        sessionmaker: ISessionMaker,
        bt: BackgroundTasks,
    ) -> None:
        async with sessionmaker() as session:
            sync_model = Synchronization(
                status=SyncStatus.IN_PROGRESS,
            )
            await self.sync_repo.add(session, sync_model)
            await session.commit()

        bt.add_task(self._sync_with_lks, sessionmaker, sync_model.id)

    async def _sync_with_lks(self, sessionmaker: ISessionMaker, sync_id: int) -> None:
        try:
            await self.lks_synchronizer.sync_structure(sessionmaker, sync_id)
            status = SyncStatus.SUCCESS
        except Exception:  # noqa: BLE001
            status = SyncStatus.FAILED

        async with sessionmaker() as session:
            await self.sync_repo.update_status(session, sync_id, status)
            await session.commit()


@lru_cache(maxsize=1)
def sync_svc() -> SyncSvc:
    return SyncSvc(
        sync_repo=sync_repo(),
        lks_api_client=lks_client(),
    )
