from unittest.mock import ANY, AsyncMock

import pytest

from app.api.schemas.base import GroupBase
from app.api.schemas.group import GroupList
from app.db.database import ISessionMaker
from app.domain.errors import NotFoundError
from app.models.group import Group
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
    expected_group = Group(
        id=group_id,
        abbr="АК1-21",
        course_id=1,
        semester_num=2,
    )
    group_repo_mock.get_by_id.return_value = expected_group

    result = await group_svc.get_group(session_maker_mock, group_id)

    assert isinstance(result, GroupBase)
    assert result.id == group_id
    assert result.abbr == expected_group.abbr
    assert result.course_id == expected_group.course_id
    assert result.semester_num == expected_group.semester_num


async def test_get_group_not_found(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_id = 999
    group_repo_mock.get_by_id.return_value = None

    with pytest.raises(NotFoundError) as excinfo:
        await group_svc.get_group(session_maker_mock, group_id)

    assert "Group not found" in str(excinfo.value)


async def test_get_groups_success(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    test_groups = [
        Group(id=1, abbr="ИУ7-11", course_id=1, semester_num=1),
        Group(id=2, abbr="ИУ7-12", course_id=1, semester_num=1),
    ]
    total_count = 2
    page = 1
    size = 10

    group_repo_mock.get_all.return_value = (test_groups, total_count)

    result = await group_svc.get_groups(
        session_maker_mock,
        page=page,
        size=size,
    )

    assert isinstance(result, GroupList)
    assert result.total == total_count
    assert result.page == page
    assert result.size == size
    assert len(result.items) == len(test_groups)
    assert all(isinstance(item, GroupBase) for item in result.items)
    assert [item.id for item in result.items] == [group.id for group in test_groups]


async def test_get_groups_with_filters(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    test_groups = [Group(id=1, abbr="ИУ7-64Б", course_id=3, semester_num=2)]
    total_count = 1

    abbr = "ИУ7-64Б"
    course = "3"
    department = "ИУ7"
    faculty = "ИУ"
    filial = "МГТУ"
    page = 1
    size = 10

    group_repo_mock.get_all.return_value = (test_groups, total_count)

    result = await group_svc.get_groups(
        session_maker_mock,
        abbr=abbr,
        course=course,
        department=department,
        faculty=faculty,
        filial=filial,
        page=page,
        size=size,
    )

    assert isinstance(result, GroupList)
    assert result.total == total_count
    assert len(result.items) == len(test_groups)

    group_repo_mock.get_all.assert_called_once_with(
        ANY,
        abbr=abbr,
        course_abbr=course,
        department_abbr=department,
        faculty_abbr=faculty,
        filial_abbr=filial,
        page=page,
        size=size,
    )


async def test_get_groups_empty_result(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: ISessionMaker,
) -> None:
    group_repo_mock.get_all.return_value = ([], 0)

    result = await group_svc.get_groups(session_maker_mock)

    assert isinstance(result, GroupList)
    assert result.total == 0
    assert len(result.items) == 0


async def test_get_group_integration(
    db_session_maker_test: ISessionMaker,
    get_or_create_group: Group,
) -> None:
    svc = GroupSvc(group_repository=group_repo())

    result = await svc.get_group(db_session_maker_test, get_or_create_group.id)

    assert isinstance(result, GroupBase)
    assert result.id == get_or_create_group.id
    assert result.abbr == get_or_create_group.abbr
    assert result.course_id == get_or_create_group.course_id
    assert result.semester_num == get_or_create_group.semester_num


async def test_get_groups_integration(
    db_session_maker_test: ISessionMaker,
    get_or_create_group: Group,
) -> None:
    svc = GroupSvc(group_repository=group_repo())

    result = await svc.get_groups(db_session_maker_test)

    assert isinstance(result, GroupList)
    assert result.total == 1
    assert len(result.items) == 1
    assert result.items[0].id == get_or_create_group.id

    filter_result = await svc.get_groups(
        db_session_maker_test,
        abbr=get_or_create_group.abbr,
    )

    assert isinstance(filter_result, GroupList)
    assert filter_result.total == 1
    assert len(filter_result.items) == 1
    assert filter_result.items[0].id == get_or_create_group.id
