import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator, Optional
from unittest.mock import AsyncMock

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

import pytest
from app.db.database import ISessionMaker, get_engine, get_session_maker
from app.models.base import Base
from app.models.course import Course
from app.models.department import Department
from app.models.faculty import Faculty
from app.models.filial import Filial
from app.models.group import Group
from app.models.synchronization import Synchronization
from app.models.teacher import Teacher
from app.models.university import University
from app.repos.course_repo import course_repo
from app.repos.department_repo import department_repo
from app.repos.faculty_repo import faculty_repo
from app.repos.filial_repo import filial_repo
from app.repos.group_repo import group_repo
from app.repos.sync_repo import sync_repo
from app.repos.teacher_repo import teacher_repo
from app.repos.university_repo import university_repo


@pytest_asyncio.fixture(scope="function", name="db_engine_test")
async def db_engine_test_fixture() -> AsyncGenerator[AsyncEngine, None]:
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture(scope="function", name="db_session_maker_test")
async def db_session_maker_test_fixture(
    db_engine_test: AsyncEngine,
) -> ISessionMaker:
    return get_session_maker(db_engine_test)


@pytest_asyncio.fixture(scope="function", name="db_session_test")
async def db_session_test_fixture(
    db_session_maker_test: ISessionMaker,
) -> AsyncGenerator[AsyncSession, None]:
    async with db_session_maker_test() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture(name="session_maker_mock")
def session_maker_mock_fixture() -> ISessionMaker:
    return get_session_maker(AsyncMock(spec=AsyncEngine))


@pytest_asyncio.fixture(scope="function", name="get_or_create_sync")
async def get_or_create_sync_fixture(db_session_test: AsyncSession) -> Synchronization:
    repo = sync_repo()
    sync: Optional[Synchronization] = await repo.get_by_id(db_session_test, 1)
    if not sync:
        sync = Synchronization(
            id=1,
            created_at=datetime.now(tz=timezone.utc),
            finished_at=datetime.now(tz=timezone.utc),
            comment="Test",
            status="success",
        )
        await repo.add(db_session_test, sync)
        await db_session_test.commit()
    return sync


@pytest_asyncio.fixture(scope="function", name="get_or_create_teacher", autouse=True)
async def get_or_create_teacher_fixture(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
) -> Teacher:
    repo = teacher_repo()
    teacher: Optional[Teacher] = await repo.get_by_id(db_session_test, 1)
    if not teacher:
        teacher = Teacher(
            id=1,
            created_at=datetime.now(tz=timezone.utc),
            lks_id=uuid.uuid4(),
            first_name="Test",
            middle_name="Test",
            last_name="Test",
            sync_id=get_or_create_sync.id,
        )
        await repo.add(db_session_test, teacher)
        await db_session_test.commit()
    return teacher


@pytest_asyncio.fixture(scope="function", name="get_or_create_university")
async def get_or_create_university_fixture(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
) -> University:
    repo = university_repo()
    university: Optional[University] = await repo.get_by_id(db_session_test, 1)
    if not university:
        university = University(
            id=1,
            lks_id=uuid.uuid4(),
            abbr="МГТУ им. Н.Э. Баумана",
            name="Московский государственный технический университет имени Баумана",
            created_at=datetime.now(tz=timezone.utc),
            sync_id=get_or_create_sync.id,
        )
        await repo.add(db_session_test, university)
        await db_session_test.commit()
    return university


@pytest_asyncio.fixture(scope="function", name="get_or_create_filial")
async def get_or_create_filial_fixture(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_university: University,
) -> Filial:
    repo = filial_repo()
    filial: Optional[Filial] = await repo.get_by_id(db_session_test, 1)
    if not filial:
        filial = Filial(
            id=1,
            created_at=datetime.now(tz=timezone.utc),
            lks_id=uuid.uuid4(),
            abbr="МГТУ им. Н.Э. Баумана",
            name="Московский государственный технический университет имени Баумана",
            university_id=get_or_create_university.id,
            sync_id=get_or_create_sync.id,
        )
        await repo.add(db_session_test, filial)
        await db_session_test.commit()
    return filial


@pytest_asyncio.fixture(scope="function", name="get_or_create_faculty")
async def get_or_create_faculty_fixture(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_filial: Filial,
) -> Faculty:
    repo = faculty_repo()
    faculty: Optional[Faculty] = await repo.get_by_id(db_session_test, 1)
    if not faculty:
        faculty = Faculty(
            id=1,
            created_at=datetime.now(tz=timezone.utc),
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
            abbr="АК",
            name="Аэрокосмический",
            filial_id=get_or_create_filial.id,
        )
        await repo.add(db_session_test, faculty)
        await db_session_test.commit()
    return faculty


@pytest_asyncio.fixture(scope="function", name="get_or_create_department")
async def get_or_create_department_fixture(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_faculty: Faculty,
) -> Department:
    repo = department_repo()
    department: Optional[Department] = await repo.get_by_id(db_session_test, 1)
    if not department:
        department = Department(
            id=1,
            created_at=datetime.now(tz=timezone.utc),
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
            abbr="АК1",
            name="СМ-2",
            faculty_id=get_or_create_faculty.id,
        )
        await repo.add(db_session_test, department)
        await db_session_test.commit()
    return department


@pytest_asyncio.fixture(scope="function", name="get_or_create_course")
async def get_or_create_course_fixture(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_department: Department,
) -> Course:
    repo = course_repo()
    course: Optional[Course] = await repo.get_by_id(db_session_test, 1)
    if not course:
        course = Course(
            id=1,
            created_at=datetime.now(tz=timezone.utc),
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
            abbr="АК1 (1 курс)",
            department_id=get_or_create_department.id,
            course_num=1,
        )
        await repo.add(db_session_test, course)
        await db_session_test.commit()
    return course


@pytest_asyncio.fixture(scope="function", name="get_or_create_group")
async def get_or_create_group_fixture(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> Group:
    repo = group_repo()
    group: Optional[Group] = await repo.get_by_id(db_session_test, 1)
    if not group:
        group = Group(
            created_at=datetime.now(tz=timezone.utc),
            sync_id=get_or_create_sync.id,
            lks_id=uuid.uuid4(),
            course_id=get_or_create_course.id,
            abbr="АК1-21",
            semester_num=2,
        )
        await repo.add(db_session_test, group)
        await db_session_test.commit()
    return group
