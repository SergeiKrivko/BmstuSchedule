# pylint: disable=too-many-locals
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
import uuid
from datetime import datetime, timezone
from unittest.mock import ANY, AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.api.schemas.group import GroupList, GroupSchedule
from app.db.database import ISessionMaker
from app.domain.errors import NotFoundError
from app.domain.schedule import ConcreteSchedulePair, GroupScheduleResult
from app.domain.timeslot import TimeSlot
from app.models.course import Course
from app.models.group import Group
from app.models.synchronization import Synchronization
from app.repos.group_repo import GroupRepo, group_repo
from app.services.group_svc import GroupSvc

pytestmark = pytest.mark.asyncio


@pytest.fixture(name="group_repo_mock")
def group_repo_mock_fixture() -> AsyncMock:
    return AsyncMock(spec=GroupRepo)


@pytest.fixture(name="group_svc")
def group_svc_fixture(group_repo_mock: AsyncMock) -> GroupSvc:
    return GroupSvc(group_repository=group_repo_mock)


async def test_get_group_success(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_id = 1
    group = Group(
        id=group_id,
        abbr="ИУ7-11",
        course_id=1,
        semester_num=2,
        lks_id=uuid.uuid4(),
        sync_id=123,
    )
    group_repo_mock.get_by_id.return_value = group

    result = await group_svc.get_group(
        sessionmaker=session_maker_mock,
        group_id=group_id,
    )

    assert result.id == group_id
    assert result.abbr == group.abbr
    assert result.course_id == group.course_id
    group_repo_mock.get_by_id.assert_called_once_with(ANY, group_id)


async def test_get_group_not_found(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_id = 1
    group_repo_mock.get_by_id.return_value = None

    with pytest.raises(NotFoundError) as excinfo:
        await group_svc.get_group(
            sessionmaker=session_maker_mock,
            group_id=group_id,
        )
    assert "Group not found" in str(excinfo.value)


async def test_get_groups_success(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    total = 3
    page = 1
    size = 10
    groups = [
        Group(
            id=1,
            abbr="ИУ7-11",
            course_id=1,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=123,
        ),
        Group(
            id=2,
            abbr="ИУ7-12",
            course_id=1,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=123,
        ),
        Group(
            id=3,
            abbr="ИУ7-13",
            course_id=1,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=123,
        ),
    ]
    group_repo_mock.get_all.return_value = (groups, total)

    result = await group_svc.get_groups(
        session_maker_mock,
        page=page,
        size=size,
    )

    assert isinstance(result, GroupList)
    assert len(result.items) == total
    assert result.total == total
    assert result.page == page
    assert result.size == size

    assert result.items[0].id == groups[0].id
    assert result.items[0].abbr == groups[0].abbr
    assert result.items[0].course_id == groups[0].course_id


async def test_get_groups_with_filters(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    abbr = "ИУ7"
    groups = [
        Group(
            id=1,
            abbr="ИУ7-11",
            course_id=1,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=123,
        ),
        Group(
            id=2,
            abbr="ИУ7-12",
            course_id=1,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=123,
        ),
    ]
    total = len(groups)
    group_repo_mock.get_all.return_value = (groups, total)

    result = await group_svc.get_groups(
        session_maker_mock,
        abbr=abbr,
    )

    assert isinstance(result, GroupList)
    assert len(result.items) == total
    assert all(group.abbr.startswith(abbr) for group in result.items)

    group_repo_mock.get_all.assert_called_once_with(
        ANY,
        abbr=abbr,
        course_abbr=None,
        department_abbr=None,
        faculty_abbr=None,
        filial_abbr=None,
        page=1,
        size=20,
    )


async def test_get_groups_empty_result(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_repo_mock.get_all.return_value = ([], 0)

    result = await group_svc.get_groups(
        session_maker_mock,
    )

    assert isinstance(result, GroupList)
    assert len(result.items) == 0
    assert result.total == 0


async def test_get_group_integration(
    db_session_test: AsyncSession,
    db_session_maker_test: ISessionMaker,
    get_or_create_course: Course,
    get_or_create_sync: Synchronization,
) -> None:
    real_repo = group_repo()
    group_service = GroupSvc(group_repository=real_repo)

    group = Group(
        id=11,
        abbr="ИУ7-11",
        course_id=get_or_create_course.id,
        semester_num=2,
        lks_id=uuid.uuid4(),
        sync_id=get_or_create_sync.id,
    )
    await real_repo.add(db_session_test, group)
    await db_session_test.commit()

    result = await group_service.get_group(
        sessionmaker=db_session_maker_test,
        group_id=group.id,
    )

    assert result.id == group.id
    assert result.abbr == group.abbr


async def test_get_groups_integration(
    db_session_test: AsyncSession,
    db_session_maker_test: ISessionMaker,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    real_repo = group_repo()
    group_service = GroupSvc(group_repository=real_repo)

    groups = [
        Group(
            id=11,
            abbr="ИУ7-11",
            course_id=get_or_create_course.id,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
        Group(
            id=12,
            abbr="ИУ7-12",
            course_id=get_or_create_course.id,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
    ]
    for group in groups:
        await real_repo.add(db_session_test, group)
    await db_session_test.commit()

    result = await group_service.get_groups(
        sessionmaker=db_session_maker_test,
    )

    assert len(result.items) == len(groups)
    assert result.total == len(groups)


async def test_get_group_schedule_success(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_id = 1

    discipline_base = DisciplineBase(
        id=1,
        full_name="Test Discipline",
        short_name="TD",
        abbr="TD",
    )

    teacher_base = TeacherBase(
        id=1,
        first_name="Test",
        middle_name="Teacher",
        last_name="Name",
        departments=[],
    )

    room_base = RoomBase(
        id=1,
        name="101",
        building="Main Building",
        map_url=None,
    )

    concrete_start = datetime(2023, 9, 18, 9, 0, tzinfo=timezone.utc)
    concrete_end = datetime(2023, 9, 18, 10, 30, tzinfo=timezone.utc)

    time_slot = TimeSlot(
        start_time=concrete_start,
        end_time=concrete_end,
    )

    group_base = GroupBase(
        id=group_id,
        abbr="ИУ7-11",
        course_id=1,
        semester_num=2,
    )

    concrete_pair = ConcreteSchedulePair(
        id=1,
        time_slot=time_slot,
        disciplines=[discipline_base],
        groups=[group_base],
        teachers=[teacher_base],
        audiences=[room_base],
    )

    schedule_result = GroupScheduleResult(
        group=group_base,
        schedule_pairs=[concrete_pair],
    )

    group_repo_mock.get_schedule_by_group_id.return_value = schedule_result

    dt_from = datetime(2023, 9, 18, 0, 0, tzinfo=timezone.utc)
    dt_to = datetime(2023, 9, 18, 23, 59, tzinfo=timezone.utc)

    result = await group_svc.get_group_schedule(
        session_maker_mock,
        group_id,
        dt_from=dt_from,
        dt_to=dt_to,
    )

    assert isinstance(result, GroupSchedule)
    assert result.group.id == group_id
    assert result.group.abbr == "ИУ7-11"

    assert len(result.schedule) == 1
    schedule_item = result.schedule[0]

    assert schedule_item.time_slot.start_time == concrete_start
    assert schedule_item.time_slot.end_time == concrete_end

    assert schedule_item.disciplines[0].id == discipline_base.id
    assert schedule_item.disciplines[0].full_name == discipline_base.full_name
    assert schedule_item.disciplines[0].short_name == discipline_base.short_name

    assert len(schedule_item.teachers) == 1
    assert schedule_item.teachers[0].id == teacher_base.id
    assert schedule_item.teachers[0].first_name == teacher_base.first_name
    assert schedule_item.teachers[0].middle_name == teacher_base.middle_name
    assert schedule_item.teachers[0].last_name == teacher_base.last_name

    assert len(schedule_item.rooms) == 1
    assert schedule_item.rooms[0].id == room_base.id
    assert schedule_item.rooms[0].name == room_base.name


async def test_get_group_schedule_not_found(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_id = 999
    group_repo_mock.get_schedule_by_group_id.return_value = None

    dt_from = datetime(2023, 9, 18, 0, 0, tzinfo=timezone.utc)
    dt_to = datetime(2023, 9, 18, 23, 59, tzinfo=timezone.utc)

    with pytest.raises(NotFoundError) as excinfo:
        await group_svc.get_group_schedule(
            session_maker_mock,
            group_id,
            dt_from=dt_from,
            dt_to=dt_to,
        )
    assert "Group schedule not found" in str(excinfo.value)


async def test_get_group_schedule_empty(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_id = 1

    group_base = GroupBase(
        id=group_id,
        abbr="ИУ7-11",
        course_id=1,
        semester_num=2,
    )

    schedule_result = GroupScheduleResult(
        group=group_base,
        schedule_pairs=[],
    )

    group_repo_mock.get_schedule_by_group_id.return_value = schedule_result

    dt_from = datetime(2023, 9, 18, 0, 0, tzinfo=timezone.utc)
    dt_to = datetime(2023, 9, 18, 23, 59, tzinfo=timezone.utc)

    result = await group_svc.get_group_schedule(
        session_maker_mock,
        group_id,
        dt_from=dt_from,
        dt_to=dt_to,
    )

    assert isinstance(result, GroupSchedule)
    assert result.group.id == group_id
    assert result.group.abbr == "ИУ7-11"
    assert len(result.schedule) == 0


async def test_get_group_schedule_with_date_filters(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_id = 1

    discipline_base = DisciplineBase(
        id=1,
        full_name="Test Discipline",
        short_name="TD",
        abbr="TD",
    )

    dt_from = datetime(2023, 9, 18, 9, 0, tzinfo=timezone.utc)
    dt_to = datetime(2023, 9, 18, 17, 0, tzinfo=timezone.utc)

    room_base = RoomBase(
        id=1,
        name="101",
        building="Main Building",
        map_url=None,
    )

    concrete_start = datetime(2023, 9, 18, 9, 0, tzinfo=timezone.utc)
    concrete_end = datetime(2023, 9, 18, 10, 30, tzinfo=timezone.utc)

    time_slot = TimeSlot(
        start_time=concrete_start,
        end_time=concrete_end,
    )

    group_base = GroupBase(
        id=group_id,
        abbr="ИУ7-11",
        course_id=1,
        semester_num=2,
    )

    concrete_pair = ConcreteSchedulePair(
        id=1,
        time_slot=time_slot,
        disciplines=[discipline_base],
        groups=[group_base],
        teachers=[],
        audiences=[room_base],
    )

    schedule_result = GroupScheduleResult(
        group=group_base,
        schedule_pairs=[concrete_pair],
    )

    group_repo_mock.get_schedule_by_group_id.return_value = schedule_result

    result = await group_svc.get_group_schedule(
        sessionmaker=session_maker_mock,
        group_id=group_id,
        dt_from=dt_from,
        dt_to=dt_to,
    )

    assert isinstance(result, GroupSchedule)
    assert result.group.id == group_id
    assert len(result.schedule) == 1

    schedule_item = result.schedule[0]
    assert schedule_item.time_slot.start_time == concrete_start
    assert schedule_item.time_slot.end_time == concrete_end

    assert group_repo_mock.get_schedule_by_group_id.call_args[0][1] == group_id
    assert group_repo_mock.get_schedule_by_group_id.call_args[1]["dt_from"] == dt_from
    assert group_repo_mock.get_schedule_by_group_id.call_args[1]["dt_to"] == dt_to
