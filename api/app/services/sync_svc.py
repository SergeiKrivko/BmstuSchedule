from functools import lru_cache
from typing import Annotated

from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.lks.client import LksClient, get_lks_client
from app.clients.lks.models import StructureNode
from app.db.database import ISessionMaker
from app.domain.sync_status import SyncStatus
from app.models.audience import Audience
from app.models.course import Course
from app.models.department import Department
from app.models.discipline import Discipline
from app.models.faculty import Faculty
from app.models.filial import Filial
from app.models.group import Group
from app.models.schedule_pair import SchedulePair
from app.models.synchronization import Synchronization
from app.models.teacher import Teacher
from app.models.university import University
from app.repos.course_repo import CourseRepo, course_repo
from app.repos.department_repo import DepartmentRepo, department_repo
from app.repos.discipline_repo import DisciplineRepo, discipline_repo
from app.repos.faculty_repo import FacultyRepo, faculty_repo
from app.repos.filial_repo import FilialRepo, filial_repo
from app.repos.group_repo import GroupRepo, group_repo
from app.repos.sync_repo import SyncRepo, sync_repo
from app.repos.teacher_repo import TeacherRepo, teacher_repo
from app.repos.university_repo import UniversityRepo, university_repo


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
        teacher_repository: TeacherRepo,
        discipline_repository: DisciplineRepo,
    ) -> None:
        self.lks_client = lks_api_client
        self.sync_repository = sync_repository
        self.group_repository = group_repository
        self.course_repository = course_repository
        self.department_repository = department_repository
        self.faculty_repository = faculty_repository
        self.filial_repository = filial_repository
        self.university_repository = university_repository
        self.teacher_repository = teacher_repository
        self.discipline_repository = discipline_repository
    async def synchronize(self, sessionmaker: ISessionMaker, sync_id: int) -> None:
        groups = await self._sync_structure(sessionmaker, sync_id)
        await self._sync_schedule(sessionmaker, sync_id, groups)

    async def _sync_structure(self, sessionmaker: ISessionMaker, sync_id: int) -> list[Group]:
        groups = []

        print("Idem na back", sync_id, flush=True)
        structure = await self.lks_client.get_structure()
        print("Structure received", sync_id, flush=True)
        async with sessionmaker() as session:
            print("University", structure.name, flush=True)
            for filial in structure.children:
                print("Filial", filial.name, flush=True)
                for faculty in filial.children:
                    print("Faculty", faculty.name, flush=True)
                    for department in faculty.children:
                        print("Department", department.name, flush=True)
                        for course in department.children:
                            print("Course", course.name, flush=True)
                            for group in course.children:
                                print("Group", group.abbr, flush=True)
                                g = await self.sync_group(session, group, sync_id)
                                groups.append(g)
            print("Synchronization finished", sync_id, flush=True)
            await session.commit()

            return groups

    async def _sync_schedule(self, sessionmaker: ISessionMaker, sync_id: int, groups: list[Group]) -> None:
        for group in groups:
            await self._sync_group_schedule(sessionmaker, sync_id, group)

    async def _sync_group_schedule(self, sessionmaker: ISessionMaker, sync_id: int, group: Group) -> None:
        try:
            schedule = await self.lks_client.get_schedule(group.lks_id)
            print("!!!", group.id, "Schedule", schedule, flush=True)
        except Exception as e:  # noqa: BLE001
            print("!!!", group.id, "Error", e, flush=True)
            return

        for pair in schedule.data:
            await self._sync_pair(sessionmaker, sync_id, pair)

    async def _sync_pair(self, sessionmaker: ISessionMaker, sync_id: int, pair) -> None:
        async with sessionmaker() as session:
            await self._sync_teachers(session, sync_id, pair.teachers)
            await self._sync_disciplines(session, sync_id, pair.discipline)
            await self._sync_audiences(session, sync_id, pair.audiences)
            await session.commit()

    async def _sync_teachers(self, session: AsyncSession, sync_id: int, teachers) -> None:
        for teacher in teachers:
            t = await self.teacher_repository.get_by_lks_id(session, teacher.id)
            if not t:
                t = Teacher(
                    first_name=teacher.first_name,
                    middle_name=teacher.middle_name,
                    last_name=teacher.last_name,
                    lks_id=teacher.id,
                )
            t.sync_id = sync_id
            await self.teacher_repository.add(session, t)

    async def _sync_audiences(self, session: AsyncSession, sync_id: int, audiences) -> None:
        for audience in audiences:
            a = await self.audience_repository.get_by_lks_id(session, audience.id)
            if not a:
                a = Audience(
                    name=audience.name,
                    lks_id=audience.id,
                    building=audience.building,
                )
            a.sync_id = sync_id
            await self.audience_repository.add(session, a)

    async def _sync_disciplines(self, session: AsyncSession, sync_id: int, disciplines) -> None:
        for discipline in disciplines:
            d = await self.discipline_repository.get_by_lks_id(session, discipline.id)
            if not d:
                d = Discipline(
                    abbr=discipline.abbr,
                    lks_id=discipline.id,
                    full_name=discipline.full_name,
                    short_name=discipline.short_name,
                    act_type=discipline.act_type,
                )
            d.sync_id = sync_id
            await self.discipline_repository.add(session, d)

    async def _sync_schedule_pair(self, session: AsyncSession, sync_id: int, pair) -> None:
        schedule_pair = SchedulePair(
            day=pair.day,
            week=pair.week,
            start_time=pair.start_time,
            end_time=pair.end_time,
            discipline_id=pair.discipline.id,
            teachers=pair.teachers,
            audiences=pair.audiences,
        )

    async def sync_group(
        self,
        session: AsyncSession,
        structure: StructureNode,
        sync_id: int,
    ) -> Group:
        g = await self.group_repository.get_by_lks_id(session, structure.id)
        print("Group", g, flush=True)
        if not g:
            g = Group(
                lks_id=structure.id,
                abbr=structure.abbr,
                semester_num=structure.semester_num or 1,
            )
        g.sync_id = sync_id
        await self.group_repository.add(session, g)
        return g

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
        lks_api_client=get_lks_client(),
        sync_repository=sync_repo(),
        group_repository=group_repo(),
        course_repository=course_repo(),
        department_repository=department_repo(),
        faculty_repository=faculty_repo(),
        filial_repository=filial_repo(),
        university_repository=university_repo(),
        teacher_repository=teacher_repo(),
        discipline_repository=discipline_repo(),
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
            print("Synchronization started", sync_model.id)

        bt.add_task(self._sync_with_lks, sessionmaker, sync_model.id)

    async def _sync_with_lks(self, sessionmaker: ISessionMaker, sync_id: int) -> None:
        try:
            print("Synchronizing with LKS", sync_id)
            await self.lks_synchronizer.synchronize(sessionmaker, sync_id)
            status = SyncStatus.SUCCESS
        except Exception as e:  # noqa: BLE001
            print("Error", e, flush=True)
            status = SyncStatus.FAILED

        async with sessionmaker() as session:
            await self.sync_repo.update_status(session, sync_id, status)
            await session.commit()


@lru_cache(maxsize=1)
def sync_svc() -> SyncSvc:
    return SyncSvc(
        sync_repo=sync_repo(),
        lks_syncer=lks_synchronizer(),
    )


SyncSvcDep = Annotated[SyncSvc, Depends(sync_svc)]
