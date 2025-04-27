# pylint: disable=too-many-lines
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-nested-blocks

import hashlib
from functools import lru_cache

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

import app.clients.lks.models as lks
from app.clients.lks.client import LksClient, get_lks_client
from app.clients.lks.models import StructureNode
from app.db.database import ISessionMaker
from app.domain.day_of_week import DayOfWeek
from app.domain.week import Week
from app.models.audience import Audience
from app.models.course import Course
from app.models.department import Department
from app.models.discipline import Discipline
from app.models.faculty import Faculty
from app.models.filial import Filial
from app.models.group import Group
from app.models.schedule_pair import SchedulePair
from app.models.teacher import Teacher
from app.models.university import University
from app.repos.audience_repo import AudienceRepo, audience_repo
from app.repos.course_repo import CourseRepo, course_repo
from app.repos.department_repo import DepartmentRepo, department_repo
from app.repos.discipline_repo import DisciplineRepo, discipline_repo
from app.repos.faculty_repo import FacultyRepo, faculty_repo
from app.repos.filial_repo import FilialRepo, filial_repo
from app.repos.group_repo import GroupRepo, group_repo
from app.repos.schedule_pair_repo import SchedulePairRepo, schedule_pair_repo
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
        audience_repository: AudienceRepo,
        schedule_pair_repository: SchedulePairRepo,
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
        self.audience_repository = audience_repository
        self.schedule_pair_repository = schedule_pair_repository

        self.__synced_audiences_cache: dict[str, Audience] = {}
        self.__synced_disciplines_cache: dict[str, Discipline] = {}
        self.__synced_teachers_cache: dict[str, Teacher] = {}

    async def synchronize(self, sessionmaker: ISessionMaker, sync_id: int) -> None:
        self.__drop_cache()

        groups = await self._sync_structure(sessionmaker, sync_id)
        await self._sync_schedule(sessionmaker, sync_id, groups)

        self.__drop_cache()

    async def _sync_structure(
        self,
        sessionmaker: ISessionMaker,
        sync_id: int,
    ) -> list[Group]:
        groups = []

        structure = await self.lks_client.get_structure()
        async with sessionmaker() as session:
            for filial in structure.children:
                for faculty in filial.children:
                    for department in faculty.children:
                        for course in department.children:
                            for group in course.children:
                                g = await self._sync_group(session, group, sync_id)
                                groups.append(g)
            await session.commit()

            return groups

    async def _sync_schedule(
        self,
        sessionmaker: ISessionMaker,
        sync_id: int,
        groups: list[Group],
    ) -> None:
        logger.info(f"Syncing schedule for {len(groups)} groups")
        for group in groups:
            await self._sync_group_schedule(sessionmaker, sync_id, group)

    async def _sync_group_schedule(
        self,
        sessionmaker: ISessionMaker,
        sync_id: int,
        group: Group,
    ) -> None:
        try:
            schedule = await self.lks_client.get_schedule(group.lks_id)
            logger.info(f"Group {group.id} - Synced schedule for {group.abbr}")
        except Exception as e:  # noqa: BLE001
            logger.error(
                f"Group {group.id} - Error syncing schedule for {group.abbr}: {e}",
            )
            return

        for pair in schedule.data:
            await self._sync_pair(sessionmaker, sync_id, pair, group)

    async def _sync_pair(
        self,
        sessionmaker: ISessionMaker,
        sync_id: int,
        pair: lks.SchedulePair,
        group: Group,
    ) -> None:
        async with sessionmaker() as session:
            teachers = await self._sync_teachers(session, sync_id, pair.teachers)
            discipline = await self._sync_discipline(session, sync_id, pair.discipline)
            audiences = await self._sync_audiences(session, sync_id, pair.audiences)
            await self._sync_schedule_pair(
                session,
                sync_id,
                pair,
                teachers,
                discipline,
                audiences,
                group,
            )
            await session.commit()

    async def _sync_teachers(
        self,
        session: AsyncSession,
        sync_id: int,
        teachers: list[lks.Teacher],
    ) -> list[Teacher]:
        logger.info("Syncing teachers")
        teacher_models = []
        for teacher in teachers:
            unique_field = str(teacher.id)
            t = self.__synced_teachers_cache.get(unique_field)
            if t:
                teacher_models.append(t)
                continue

            t = await self.teacher_repository.get_by_lks_id(session, teacher.id)
            if not t:
                t = Teacher(
                    first_name=teacher.first_name,
                    middle_name=teacher.middle_name,
                    last_name=teacher.last_name,
                    lks_id=teacher.id,
                )
            t.sync_id = sync_id
            self.__synced_teachers_cache[unique_field] = t
            teacher_models.append(t)
            await self.teacher_repository.add(session, t)
        return teacher_models

    async def _sync_audiences(
        self,
        session: AsyncSession,
        sync_id: int,
        audiences: list[lks.Audience],
    ) -> list[Audience]:
        logger.info("Syncing audiences")
        audience_models = []
        for audience in audiences:
            # у аудиторий может не быть lks_id, поэтому смотрим также на name и building
            unique_field = (
                hashlib.md5(  # noqa: S324  безопасно, т.к. хеш только для поиска
                    f"{audience.id}_{audience.name}_{audience.building}".encode(),
                ).hexdigest()
            )
            a = self.__synced_audiences_cache.get(unique_field)
            if a:
                audience_models.append(a)
                continue

            a = await self.audience_repository.get_by_unique_field(
                session,
                unique_field,
            )
            if not a:
                a = Audience(
                    name=audience.name,
                    lks_id=audience.id,
                    building=audience.building,
                    unique_field=unique_field,
                )
            a.sync_id = sync_id
            self.__synced_audiences_cache[unique_field] = a
            audience_models.append(a)
            await self.audience_repository.add(session, a)
        return audience_models

    async def _sync_discipline(
        self,
        session: AsyncSession,
        sync_id: int,
        discipline: lks.Discipline,
    ) -> Discipline:
        logger.info(f"Syncing discipline {discipline.abbr}")
        unique_field = hashlib.md5(  # noqa: S324  безопасно, т.к. хеш только для поиска
            f"{discipline.abbr}_{discipline.act_type}".encode(),
        ).hexdigest()
        d = self.__synced_disciplines_cache.get(unique_field)
        if d:
            return d

        d = await self.discipline_repository.get_by_unique_field(session, unique_field)
        if not d:
            d = Discipline(
                abbr=discipline.abbr,
                full_name=discipline.full_name,
                short_name=discipline.short_name,
                act_type=discipline.act_type,
                unique_field=unique_field,
            )
        d.sync_id = sync_id
        self.__synced_disciplines_cache[unique_field] = d
        await self.discipline_repository.add(session, d)
        return d

    async def _sync_schedule_pair(
        self,
        session: AsyncSession,
        sync_id: int,
        pair: lks.SchedulePair,
        teachers: list[Teacher],
        discipline: Discipline,
        audiences: list[Audience],
        group: Group,
    ) -> None:
        logger.info(f"Syncing schedule pair {pair.discipline.abbr} {group.abbr}")

        # считаем, что пары совпадают, если они проходят в одно время в одном месте
        day = DayOfWeek.from_lks(pair.day)
        week = Week.from_lks(pair.week)
        start_time = pair.start_time
        end_time = pair.end_time
        audience_ids = sorted(a.id for a in audiences)
        unique_field = hashlib.md5(  # noqa: S324  безопасно, т.к. хеш только для поиска
            f"{day}_{week}_{start_time}_{end_time}_{audience_ids}".encode(),
        ).hexdigest()

        sp = await self.schedule_pair_repository.get_by_unique_field(
            session,
            unique_field,
        )
        if not sp:
            sp = SchedulePair(
                day=day,
                week=week,
                start_time=start_time,
                end_time=end_time,
                discipline_id=discipline.id,
                groups=[group],
                teachers=teachers,
                audiences=audiences,
                sync_id=sync_id,
                unique_field=unique_field,
            )
        await self.schedule_pair_repository.add(session, sp)

    async def _sync_group(
        self,
        session: AsyncSession,
        structure: StructureNode,
        sync_id: int,
    ) -> Group:
        logger.info(f"Syncing group {structure.abbr}")
        g = await self.group_repository.get_by_lks_id(session, structure.id)
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

    def __drop_cache(self) -> None:
        self.__synced_audiences_cache.clear()
        self.__synced_disciplines_cache.clear()
        self.__synced_teachers_cache.clear()


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
        audience_repository=audience_repo(),
        schedule_pair_repository=schedule_pair_repo(),
    )
