from datetime import datetime, timedelta
from typing import Sequence

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.api.schemas.schedule_pair import SchedulePairRead
from app.domain.day_of_week import DayOfWeek
from app.domain.timeslot import TimeSlot
from app.domain.week import Week
from app.models.schedule_pair import SchedulePair


def generate_concrete_pairs(
    schedule_pairs: Sequence[SchedulePair],
    dt_from: datetime,
    dt_to: datetime,
) -> list[SchedulePairRead]:
    """Generate concrete schedule pairs with specific dates."""
    concrete_pairs = []
    current_date = dt_from.replace(hour=0, minute=0, second=0, microsecond=0)

    while dt_to - current_date >= timedelta(days=1):
        concrete_pairs.extend(
            generate_concrete_pairs_for_date(
                schedule_pairs,
                current_date,
                dt_from,
                dt_to,
            ),
        )
        current_date += timedelta(days=1)
    return concrete_pairs


def generate_concrete_pairs_for_date(
    schedule_pairs: Sequence[SchedulePair],
    current_date: datetime,
    dt_from: datetime,
    dt_to: datetime,
) -> list[SchedulePairRead]:
    """Generate concrete schedule pairs for a specific date."""
    week = Week.from_datetime(current_date)
    day_of_week = DayOfWeek.from_datetime(current_date)

    concrete_pairs = []
    for pair in schedule_pairs:
        if DayOfWeek(pair.day) != day_of_week:
            continue

        if not Week(pair.week).match(week):
            continue

        start_hour, start_minute = map(int, pair.start_time.split(":"))
        end_hour, end_minute = map(int, pair.end_time.split(":"))

        concrete_start = current_date.replace(
            hour=start_hour,
            minute=start_minute,
            second=0,
            microsecond=0,
        )
        concrete_end = current_date.replace(
            hour=end_hour,
            minute=end_minute,
            second=0,
            microsecond=0,
        )

        if concrete_end < dt_from or concrete_start > dt_to:
            continue

        concrete_pair = SchedulePairRead(
            id=pair.id,
            time_slot=TimeSlot(
                start_time=concrete_start,
                end_time=concrete_end,
            ),
            disciplines=[
                DisciplineBase(
                    id=pair.discipline.id,
                    abbr=pair.discipline.abbr,
                    full_name=pair.discipline.full_name,
                    short_name=pair.discipline.short_name,
                    act_type=pair.discipline.act_type,
                ),
            ],
            teachers=[
                TeacherBase(
                    id=teacher.id,
                    first_name=teacher.first_name,
                    middle_name=teacher.middle_name,
                    last_name=teacher.last_name,
                    # todo либо убрать это поле, либо добавить джойны
                    departments=[],
                )
                for teacher in pair.teachers
            ],
            rooms=[
                RoomBase(
                    id=audience.id,
                    name=audience.name,
                    building=audience.building,
                    map_url=audience.map_url,
                )
                for audience in pair.audiences
            ],
            groups=[
                GroupBase(
                    id=group.id,
                    abbr=group.abbr,
                    course_id=group.course_id,
                    semester_num=group.semester_num,
                )
                for group in pair.groups
            ],
        )
        concrete_pairs.append(concrete_pair)

    return concrete_pairs
