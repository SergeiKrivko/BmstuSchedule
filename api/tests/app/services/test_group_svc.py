from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.api.schemas.base import GroupBase
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
    session_maker_mock: async_sessionmaker[AsyncSession],
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
    assert result.id == expected_group.id
    assert result.abbr == expected_group.abbr
    assert result.course_id == expected_group.course_id
    assert result.semester_num == expected_group.semester_num


async def test_get_group_not_found(
    group_svc: GroupSvc,
    group_repo_mock: AsyncMock,
    session_maker_mock: async_sessionmaker[AsyncSession],
) -> None:
    group_id = 999
    group_repo_mock.get_by_id.return_value = None

    with pytest.raises(NotFoundError) as excinfo:
        await group_svc.get_group(session_maker_mock, group_id)

    assert "Group not found" in str(excinfo.value)


async def test_get_group_integration(
    db_session_maker_test: async_sessionmaker[AsyncSession],
    get_or_create_group: Group,
) -> None:
    svc = GroupSvc(group_repository=group_repo())

    result = await svc.get_group(db_session_maker_test, get_or_create_group.id)

    assert isinstance(result, GroupBase)
    assert result.id == get_or_create_group.id
    assert result.abbr == get_or_create_group.abbr
    assert result.course_id == get_or_create_group.course_id
    assert result.semester_num == get_or_create_group.semester_num
