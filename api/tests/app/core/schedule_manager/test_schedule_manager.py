from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

from app import domain
from app.api import schemas
from app.api.schemas.schedule_pair import SchedulePairRead
from app.clients.lks.models import CurrentSchedule, WeekRu
from app.core.schedule_manager import InvalidTimeFormatError, ScheduleManager
from app.models.discipline import Discipline
from app.models.schedule_pair import SchedulePair

pytestmark = pytest.mark.asyncio


async def test_generate_concrete_pairs_basic(
    schedule_manager: ScheduleManager,
    mock_schedule_pair: SchedulePair,
    mock_discipline_base: schemas.DisciplineBase,
    mock_group_base: schemas.GroupBase,
    mock_teacher_base: schemas.TeacherBase,
    mock_room_base: schemas.RoomBase,
    monday_time_slot: domain.TimeSlot,
    mock_start_hour: int,
    mock_start_minute: int,
    mock_end_hour: int,
    mock_end_minute: int,
) -> None:
    result = await schedule_manager.generate_concrete_pairs(
        schedule_pairs=[mock_schedule_pair],
        dt_from=monday_time_slot.start_time,
        dt_to=monday_time_slot.end_time,
    )

    expected_result = [
        SchedulePairRead(
            time_slot=domain.TimeSlot(
                start_time=monday_time_slot.start_time.replace(
                    hour=mock_start_hour,
                    minute=mock_start_minute,
                ),
                end_time=monday_time_slot.end_time.replace(
                    hour=mock_end_hour,
                    minute=mock_end_minute,
                ),
            ),
            discipline=mock_discipline_base,
            groups=[mock_group_base],
            teachers=[mock_teacher_base],
            rooms=[mock_room_base],
        ),
    ]

    assert result == expected_result


async def test_generate_concrete_pairs_wrong_day(
    schedule_manager: ScheduleManager,
    mock_schedule_pair: SchedulePair,
    tuesday_time_slot: domain.TimeSlot,
) -> None:
    result = await schedule_manager.generate_concrete_pairs(
        schedule_pairs=[mock_schedule_pair],
        dt_from=tuesday_time_slot.start_time,
        dt_to=tuesday_time_slot.end_time,
    )

    assert len(result) == 0


async def test_generate_concrete_pairs_wrong_week(
    schedule_manager: ScheduleManager,
    lks_client_mock: AsyncMock,
    mock_schedule_pair: SchedulePair,
    monday_time_slot: domain.TimeSlot,
) -> None:
    lks_client_mock.get_current_schedule.return_value = CurrentSchedule(
        term=1,
        weekNumber=2,
        weekShortName=WeekRu.EVEN,
        semesterStarts=datetime.now(tz=timezone.utc).date(),
        semesterEnds=datetime.now(tz=timezone.utc).date() + timedelta(days=30),
    )

    result = await schedule_manager.generate_concrete_pairs(
        schedule_pairs=[mock_schedule_pair],
        dt_from=monday_time_slot.start_time,
        dt_to=monday_time_slot.end_time,
    )

    assert len(result) == 0


async def test_generate_concrete_pairs_time_range(
    schedule_manager: ScheduleManager,
    mock_schedule_pair: SchedulePair,
    mock_discipline_base: schemas.DisciplineBase,
    mock_group_base: schemas.GroupBase,
    mock_teacher_base: schemas.TeacherBase,
    mock_room_base: schemas.RoomBase,
    mock_start_hour: int,
    mock_start_minute: int,
    mock_end_hour: int,
    mock_end_minute: int,
) -> None:
    dt_from = datetime(2024, 3, 18, 11, 0, tzinfo=timezone.utc)  # monday 11:00
    dt_to = datetime(2024, 3, 18, 12, 0, tzinfo=timezone.utc)  # monday 12:00

    result = await schedule_manager.generate_concrete_pairs(
        schedule_pairs=[mock_schedule_pair],
        dt_from=dt_from,
        dt_to=dt_to,
    )

    expected_result = [
        SchedulePairRead(
            time_slot=domain.TimeSlot(
                start_time=dt_from.replace(
                    hour=mock_start_hour,
                    minute=mock_start_minute,
                ),
                end_time=dt_from.replace(
                    hour=mock_end_hour,
                    minute=mock_end_minute,
                ),
            ),
            discipline=mock_discipline_base,
            groups=[mock_group_base],
            teachers=[mock_teacher_base],
            rooms=[mock_room_base],
        ),
    ]

    assert result == expected_result


async def test_generate_concrete_pairs_odd_week(
    schedule_manager: ScheduleManager,
    mock_schedule_pair: SchedulePair,
    mock_discipline_base: schemas.DisciplineBase,
    mock_group_base: schemas.GroupBase,
    mock_teacher_base: schemas.TeacherBase,
    mock_room_base: schemas.RoomBase,
    mock_start_hour: int,
    mock_start_minute: int,
    mock_end_hour: int,
    mock_end_minute: int,
) -> None:
    dt_from = datetime(2024, 3, 18, 0, 0, tzinfo=timezone.utc)  # monday
    dt_to = datetime(2024, 3, 25, 23, 59, tzinfo=timezone.utc)  # next monday

    result = await schedule_manager.generate_concrete_pairs(
        schedule_pairs=[mock_schedule_pair],
        dt_from=dt_from,
        dt_to=dt_to,
    )

    expected_result = [
        SchedulePairRead(
            time_slot=domain.TimeSlot(
                start_time=dt_from.replace(
                    hour=mock_start_hour,
                    minute=mock_start_minute,
                ),
                end_time=dt_from.replace(hour=mock_end_hour, minute=mock_end_minute),
            ),
            discipline=mock_discipline_base,
            groups=[mock_group_base],
            teachers=[mock_teacher_base],
            rooms=[mock_room_base],
        ),
    ]

    assert result == expected_result


async def test_generate_concrete_pairs_all_week(
    schedule_manager: ScheduleManager,
    mock_schedule_pair: SchedulePair,
    mock_discipline_base: schemas.DisciplineBase,
    mock_group_base: schemas.GroupBase,
    mock_teacher_base: schemas.TeacherBase,
    mock_room_base: schemas.RoomBase,
    mock_start_hour: int,
    mock_start_minute: int,
    mock_end_hour: int,
    mock_end_minute: int,
) -> None:
    mock_schedule_pair.week = domain.Week.ALL.value
    dt_from = datetime(2024, 3, 18, 0, 0, tzinfo=timezone.utc)  # monday
    dt_to = datetime(2024, 3, 25, 23, 59, tzinfo=timezone.utc)  # next monday

    result = await schedule_manager.generate_concrete_pairs(
        schedule_pairs=[mock_schedule_pair],
        dt_from=dt_from,
        dt_to=dt_to,
    )

    expected_result = [
        SchedulePairRead(
            time_slot=domain.TimeSlot(
                start_time=dt_from.replace(
                    hour=mock_start_hour,
                    minute=mock_start_minute,
                ),
                end_time=dt_from.replace(hour=mock_end_hour, minute=mock_end_minute),
            ),
            discipline=mock_discipline_base,
            groups=[mock_group_base],
            teachers=[mock_teacher_base],
            rooms=[mock_room_base],
        ),
        SchedulePairRead(
            time_slot=domain.TimeSlot(
                start_time=dt_to.replace(
                    hour=mock_start_hour,
                    minute=mock_start_minute,
                ),
                end_time=dt_to.replace(
                    hour=mock_end_hour,
                    minute=mock_end_minute,
                ),
            ),
            discipline=mock_discipline_base,
            groups=[mock_group_base],
            teachers=[mock_teacher_base],
            rooms=[mock_room_base],
        ),
    ]

    assert result == expected_result


async def test_generate_concrete_pairs_empty_input(
    schedule_manager: ScheduleManager,
    monday_time_slot: domain.TimeSlot,
) -> None:
    result = await schedule_manager.generate_concrete_pairs(
        schedule_pairs=[],
        dt_from=monday_time_slot.start_time,
        dt_to=monday_time_slot.end_time,
    )

    assert len(result) == 0


async def test_generate_concrete_pairs_invalid_time_format(
    schedule_manager: ScheduleManager,
    mock_discipline: Discipline,
    monday_time_slot: domain.TimeSlot,
) -> None:
    invalid_pair = SchedulePair(
        id=1,
        day=domain.DayOfWeek.MONDAY.value,
        week=domain.Week.ODD.value,
        start_time="invalid",
        end_time="invalid",
        discipline=mock_discipline,
        groups=[],
        teachers=[],
        audiences=[],
        unique_field="test",
    )

    with pytest.raises(InvalidTimeFormatError):
        await schedule_manager.generate_concrete_pairs(
            schedule_pairs=[invalid_pair],
            dt_from=monday_time_slot.start_time,
            dt_to=monday_time_slot.end_time,
        )
