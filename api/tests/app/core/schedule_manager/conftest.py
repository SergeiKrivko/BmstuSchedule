from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

from app import domain
from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.clients import lks
from app.core.schedule_manager import ScheduleManager
from app.models.audience import Audience
from app.models.discipline import Discipline
from app.models.group import Group
from app.models.schedule_pair import SchedulePair
from app.models.teacher import Teacher


@pytest.fixture(name="lks_client_mock")
def lks_client_mock_fixture() -> AsyncMock:
    client = AsyncMock(spec=lks.LksClient)
    client.get_current_schedule.return_value = lks.CurrentSchedule(
        term=1,
        weekNumber=1,
        weekShortName=lks.WeekRu.ODD,
        semesterStarts=datetime.now(tz=timezone.utc).date(),
        semesterEnds=datetime.now(tz=timezone.utc).date() + timedelta(days=30),
    )
    return client


@pytest.fixture(name="schedule_manager")
def schedule_manager_fixture(lks_client_mock: AsyncMock) -> ScheduleManager:
    return ScheduleManager(lks_client=lks_client_mock)


@pytest.fixture(name="monday_time_slot")
def monday_time_slot_fixture() -> domain.TimeSlot:
    return domain.TimeSlot(
        start_time=datetime(2024, 3, 18, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2024, 3, 18, 23, 59, tzinfo=timezone.utc),
    )


@pytest.fixture(name="tuesday_time_slot")
def tuesday_time_slot_fixture() -> domain.TimeSlot:
    return domain.TimeSlot(
        start_time=datetime(2024, 3, 19, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2024, 3, 19, 23, 59, tzinfo=timezone.utc),
    )


@pytest.fixture(name="mock_discipline")
def mock_discipline_fixture() -> Discipline:
    return Discipline(
        id=1,
        abbr="TEST",
        full_name="Test Discipline",
        short_name="Test",
        act_type="lecture",
    )


@pytest.fixture(name="mock_discipline_base")
def mock_discipline_base_fixture(mock_discipline: Discipline) -> DisciplineBase:
    return DisciplineBase(
        id=mock_discipline.id,
        abbr=mock_discipline.abbr,
        full_name=mock_discipline.full_name,
        short_name=mock_discipline.short_name,
        act_type=mock_discipline.act_type,
    )


@pytest.fixture(name="mock_group")
def mock_group_fixture() -> Group:
    return Group(
        id=1,
        abbr="TEST-101",
        course_id=1,
        semester_num=1,
    )


@pytest.fixture(name="mock_group_base")
def mock_group_base_fixture(mock_group: Group) -> GroupBase:
    return GroupBase(
        id=mock_group.id,
        abbr=mock_group.abbr,
        course_id=mock_group.course_id,
        semester_num=mock_group.semester_num,
    )


@pytest.fixture(name="mock_teacher")
def mock_teacher_fixture() -> Teacher:
    return Teacher(
        id=1,
        first_name="John",
        middle_name="Middle",
        last_name="Doe",
    )


@pytest.fixture(name="mock_teacher_base")
def mock_teacher_base_fixture(mock_teacher: Teacher) -> TeacherBase:
    return TeacherBase(
        id=mock_teacher.id,
        first_name=mock_teacher.first_name,
        middle_name=mock_teacher.middle_name,
        last_name=mock_teacher.last_name,
    )


@pytest.fixture(name="mock_audience")
def mock_audience_fixture() -> Audience:
    return Audience(
        id=1,
        name="101",
        building="Main",
    )


@pytest.fixture(name="mock_room_base")
def mock_room_base_fixture(mock_audience: Audience) -> RoomBase:
    return RoomBase(
        id=mock_audience.id,
        name=mock_audience.name,
        building=mock_audience.building,
    )


@pytest.fixture(name="mock_start_hour")
def mock_start_hour_fixture() -> int:
    return 10


@pytest.fixture(name="mock_start_minute")
def mock_start_minute_fixture() -> int:
    return 0


@pytest.fixture(name="mock_end_hour")
def mock_end_hour_fixture() -> int:
    return 11


@pytest.fixture(name="mock_end_minute")
def mock_end_minute_fixture() -> int:
    return 30


@pytest.fixture(name="mock_schedule_pair")
def mock_schedule_pair_fixture(
    mock_discipline: Discipline,
    mock_group: Group,
    mock_teacher: Teacher,
    mock_audience: Audience,
    mock_start_hour: int,
    mock_start_minute: int,
    mock_end_hour: int,
    mock_end_minute: int,
) -> SchedulePair:
    return SchedulePair(
        id=1,
        day=domain.DayOfWeek.MONDAY.value,
        week=domain.Week.ODD.value,
        start_time=f"{mock_start_hour}:{mock_start_minute}",
        end_time=f"{mock_end_hour}:{mock_end_minute}",
        discipline=mock_discipline,
        groups=[mock_group],
        teachers=[mock_teacher],
        audiences=[mock_audience],
        unique_field="test",
    )
