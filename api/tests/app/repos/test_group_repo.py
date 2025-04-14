import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.models.group import Group
from app.models.synchronization import Synchronization
from app.repos.group_repo import group_repo

pytestmark = pytest.mark.asyncio


async def test_get_all_no_filters(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    repo = group_repo()

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
        await repo.add(db_session_test, group)
    await db_session_test.commit()

    selected_groups, selected_total = await repo.get_all(db_session_test)

    assert total == selected_total
    assert len(selected_groups) == len(groups)
    assert [g.id for g in selected_groups] == [g.id for g in groups]


async def test_get_all_with_pagination(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    repo = group_repo()
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
        await repo.add(db_session_test, group)
    await db_session_test.commit()

    page_size = 2

    page1, total1 = await repo.get_all(
        db_session_test,
        page=1,
        size=page_size,
    )

    assert len(page1) == page_size
    assert total1 == len(groups)

    page2, total2 = await repo.get_all(
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
    repo = group_repo()

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
        await repo.add(db_session_test, group)
    await db_session_test.commit()

    filter_abbr = groups[0].abbr

    filtered_groups, total = await repo.get_all(
        db_session_test,
        abbr=filter_abbr,
    )

    assert total == 1
    assert len(filtered_groups) == 1
    assert filtered_groups[0].id == groups[0].id


async def test_get_order_by_created_at(
    db_session_test: AsyncSession,
    get_or_create_sync: Synchronization,
    get_or_create_course: Course,
) -> None:
    repo = group_repo()
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
        await repo.add(db_session_test, group)
    await db_session_test.commit()

    selected_groups, total = await repo.get_all(
        db_session_test,
    )

    assert total == len(groups)
    assert selected_groups[0].id == groups[1].id
    assert selected_groups[1].id == groups[2].id
    assert selected_groups[2].id == groups[0].id


async def test_get_all_empty_result(
    db_session_test: AsyncSession,
) -> None:
    repo = group_repo()
    groups, total = await repo.get_all(
        db_session_test,
        abbr="NO_SUCH_GROUP_EXISTS",
    )

    assert len(groups) == 0
    assert total == 0
