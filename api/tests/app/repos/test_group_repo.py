# pylint: disable=too-many-lines
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.week import Week
from app.models.audience import Audience
from app.models.course import Course
from app.models.department import Department
from app.models.discipline import Discipline
from app.models.group import Group
from app.models.schedule_pair import SchedulePair
from app.models.synchronization import Synchronization
from app.repos.audience_repo import audience_repo
from app.repos.course_repo import course_repo
from app.repos.discipline_repo import discipline_repo
from app.repos.group_repo import group_repo
from app.repos.schedule_pair_repo import schedule_pair_repo

pytestmark = pytest.mark.asyncio


async def test_get_group_by_id_success(
    db_session_test: AsyncSession,
    get_or_create_group: Group,
) -> None:
    group_repository = group_repo()
    group = await group_repository.get_by_id(db_session_test, get_or_create_group.id)
    assert group is not None
    assert group.id == get_or_create_group.id


async def test_get_all_no_filters(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    group_repository = group_repo()

    groups = [
        Group(
            abbr=f"ИУ7-64Б-{i}-unique-abbr1",
            course_id=get_or_create_course.id,
            semester_num=2,
            sync_id=get_or_create_sync.id,
            lks_id=uuid.uuid4(),
        )
        for i in range(1, 11)
    ]
    total = 10
    for group in groups:
        await group_repository.add(db_session_test, group)
    await db_session_test.commit()

    selected_groups, selected_total = await group_repository.get_all(db_session_test)

    assert total == selected_total
    assert len(selected_groups) == len(groups)
    assert [g.id for g in selected_groups] == [g.id for g in groups]


async def test_get_all_with_pagination(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    group_repository = group_repo()
    groups = [
        Group(
            abbr=f"ИУ7-64Б-{i}-unique-abbr2",
            course_id=get_or_create_course.id,
            semester_num=2,
            sync_id=get_or_create_sync.id,
            lks_id=uuid.uuid4(),
        )
        for i in range(1, 6)
    ]
    for group in groups:
        await group_repository.add(db_session_test, group)
    await db_session_test.commit()

    page_size = 2

    page1, total1 = await group_repository.get_all(
        db_session_test,
        page=1,
        size=page_size,
    )

    assert len(page1) == page_size
    assert total1 == len(groups)

    page2, total2 = await group_repository.get_all(
        db_session_test,
        page=2,
        size=page_size,
    )

    assert len(page2) == page_size
    assert total2 == len(groups)

    assert total1 == total2
    assert len({g.id for g in page1}.intersection({g.id for g in page2})) == 0


async def test_get_all_with_abbr_filter(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    group_repository = group_repo()

    groups = [
        Group(
            abbr="ИУ7-64Б-unique-abbr3",
            course_id=get_or_create_course.id,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
        Group(
            abbr="ИУ7-64В",
            course_id=get_or_create_course.id,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
    ]
    for group in groups:
        await group_repository.add(db_session_test, group)
    await db_session_test.commit()

    filter_abbr = groups[0].abbr

    filtered_groups, total = await group_repository.get_all(
        db_session_test,
        abbr=filter_abbr,
    )

    assert total == 1
    assert len(filtered_groups) == 1
    assert filtered_groups[0].id == groups[0].id


async def test_get_all_with_course_abbr_filter(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_department: Department,
) -> None:
    course_repository = course_repo()
    courses = [
        Course(
            abbr="АК1 (1 курс)",
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
            course_num=1,
            department_id=get_or_create_department.id,
        ),
        Course(
            abbr="АК2 (1 курс)",
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
            course_num=1,
            department_id=get_or_create_department.id,
        ),
    ]
    for course in courses:
        await course_repository.add(db_session_test, course)
    await db_session_test.commit()

    group_repository = group_repo()
    groups = [
        Group(
            abbr="ИУ7-64Б-unique-abbr7",
            course_id=courses[0].id,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
        Group(
            abbr="ИУ7-64Б-unique-abbr8",
            course_id=courses[1].id,
            semester_num=2,
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
    ]
    for group in groups:
        await group_repository.add(db_session_test, group)
    await db_session_test.commit()

    filter_course_abbr = groups[0].course.abbr

    filtered_groups, total = await group_repository.get_all(
        db_session_test,
        course_abbr=filter_course_abbr,
    )

    assert total == 1
    assert len(filtered_groups) == 1
    assert filtered_groups[0].id == groups[0].id


async def test_get_order_by_created_at(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    group_repository = group_repo()
    groups = [
        Group(
            abbr="ИУ7-64Б-1-unique-abbr4",
            course_id=get_or_create_course.id,
            semester_num=2,
            created_at=datetime.now(tz=timezone.utc) - timedelta(seconds=25),
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
        Group(
            abbr="ИУ7-64Б-2-unique-abbr5",
            course_id=get_or_create_course.id,
            semester_num=2,
            created_at=datetime.now(tz=timezone.utc),
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
        Group(
            abbr="ИУ7-64Б-3-unique-abbr6",
            course_id=get_or_create_course.id,
            semester_num=2,
            created_at=datetime.now(tz=timezone.utc) - timedelta(seconds=5),
            lks_id=uuid.uuid4(),
            sync_id=get_or_create_sync.id,
        ),
    ]
    for group in groups:
        await group_repository.add(db_session_test, group)
    await db_session_test.commit()

    selected_groups, total = await group_repository.get_all(
        db_session_test,
    )

    assert total == len(groups)
    assert selected_groups[0].id == groups[1].id
    assert selected_groups[1].id == groups[2].id
    assert selected_groups[2].id == groups[0].id


async def test_get_all_empty_result(
    db_session_test: AsyncSession,
) -> None:
    group_repository = group_repo()
    groups, total = await group_repository.get_all(
        db_session_test,
        abbr="NO_SUCH_GROUP_EXISTS",
    )

    assert len(groups) == 0
    assert total == 0


async def test_get_schedule_by_group_id_success(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    group_repository = group_repo()
    discipline_repository = discipline_repo()
    audience_repository = audience_repo()
    schedule_pair_repository = schedule_pair_repo()

    group = Group(
        abbr="ИУ7-64Б-test-schedule",
        course_id=get_or_create_course.id,
        semester_num=2,
        sync_id=get_or_create_sync.id,
        lks_id=uuid.uuid4(),
    )
    await group_repository.add(db_session_test, group)

    discipline = Discipline(
        full_name="Test Discipline",
        short_name="TD",
        abbr="TD",
        sync_id=get_or_create_sync.id,
        lks_id=uuid.uuid4(),
    )
    await discipline_repository.add(db_session_test, discipline)

    audience = Audience(
        name="Test Audience",
        building="Test Building",
        sync_id=get_or_create_sync.id,
        lks_id=uuid.uuid4(),
    )
    await audience_repository.add(db_session_test, audience)

    schedule_pair = SchedulePair(
        day="monday",
        week=Week.ALL.value,
        start_time="09:00",
        end_time="10:30",
        discipline_id=discipline.id,
        sync_id=get_or_create_sync.id,
    )
    await schedule_pair_repository.add(db_session_test, schedule_pair)

    # Add directly to avoid lazy loading issues
    await db_session_test.execute(
        text(
            """
        INSERT INTO schedule_pair_group (schedule_pair_id, group_id)
        VALUES (:schedule_pair_id, :group_id)
        """,
        ),
        {"schedule_pair_id": schedule_pair.id, "group_id": group.id},
    )

    await db_session_test.execute(
        text(
            """
        INSERT INTO schedule_pair_audience (schedule_pair_id, audience_id)
        VALUES (:schedule_pair_id, :audience_id)
        """,
        ),
        {"schedule_pair_id": schedule_pair.id, "audience_id": audience.id},
    )

    await db_session_test.commit()

    dt_from = datetime(2025, 4, 21, tzinfo=timezone.utc)
    dt_to = datetime(2025, 4, 22, tzinfo=timezone.utc)

    result = await group_repository.get_schedule_by_group_id(
        db_session_test,
        group.id,
        dt_from=dt_from,
        dt_to=dt_to,
    )

    assert result is not None
    assert result.group.id == group.id
    assert result.schedule_pairs[0].id == schedule_pair.id


async def test_get_schedule_by_group_id_not_found(
    db_session_test: AsyncSession,
) -> None:
    group_repository = group_repo()

    dt_from = datetime(2025, 4, 21, tzinfo=timezone.utc)
    dt_to = datetime(2025, 4, 22, tzinfo=timezone.utc)

    result = await group_repository.get_schedule_by_group_id(
        db_session_test,
        999999,
        dt_from=dt_from,
        dt_to=dt_to,
    )

    assert result is None


async def test_get_schedule_by_group_id_empty_schedule(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    group_repository = group_repo()

    group = Group(
        abbr="ИУ7-64Б-test-empty-schedule",
        course_id=get_or_create_course.id,
        semester_num=2,
        sync_id=get_or_create_sync.id,
        lks_id=uuid.uuid4(),
    )
    await group_repository.add(db_session_test, group)
    await db_session_test.commit()

    dt_from = datetime(2025, 4, 21, tzinfo=timezone.utc)
    dt_to = datetime(2025, 4, 22, tzinfo=timezone.utc)

    result = await group_repository.get_schedule_by_group_id(
        session=db_session_test,
        group_id=group.id,
        dt_from=dt_from,
        dt_to=dt_to,
    )

    assert result is not None
    assert result.group.id == group.id
    assert len(result.schedule_pairs) == 0
