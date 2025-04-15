from datetime import datetime, timedelta
from functools import lru_cache
from typing import List, Optional, Sequence, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import count

from app.api.schemas.base import DisciplineBase, GroupBase, RoomBase, TeacherBase
from app.domain.day_of_week import DayOfWeek
from app.domain.schedule import ConcreteSchedulePair, GroupScheduleResult
from app.domain.timeslot import TimeSlot
from app.domain.week import Week
from app.models.course import Course
from app.models.group import Group
from app.models.many_to_many import schedule_pair_group
from app.models.schedule_pair import SchedulePair
from app.repos.base_repo import BaseRepo


def _generate_concrete_pairs(
    schedule_pairs: List[SchedulePair],
    dt_from: datetime,
    dt_to: datetime,
) -> List[ConcreteSchedulePair]:
    """Generate concrete schedule pairs with specific dates."""
    concrete_pairs = []
    current_date = dt_from.replace(hour=0, minute=0, second=0, microsecond=0)

    while dt_to - current_date >= timedelta(days=1):
        week = Week.from_datetime(current_date)
        day_of_week = DayOfWeek.from_datetime(current_date)

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

            concrete_pair = ConcreteSchedulePair(
                id=pair.id,
                time_slot=TimeSlot(
                    start_time=concrete_start,
                    end_time=concrete_end,
                ),
                discipline=DisciplineBase(
                    id=pair.discipline.id,
                    abbr=pair.discipline.abbr,
                    full_name=pair.discipline.full_name,
                    short_name=pair.discipline.short_name,
                    act_type=pair.discipline.act_type,
                ),
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
                audiences=[
                    RoomBase(
                        id=audience.id,
                        name=audience.name,
                        building=audience.building,
                        map_url=audience.map_url,
                    )
                    for audience in pair.audiences
                ],
            )
            concrete_pairs.append(concrete_pair)

        current_date += timedelta(days=1)

    return concrete_pairs


class GroupRepo(BaseRepo[Group]):
    model = Group

    async def get_all(
        self,
        session: AsyncSession,
        abbr: Optional[str] = None,
        course_abbr: Optional[str] = None,
        department_abbr: Optional[str] = None,
        faculty_abbr: Optional[str] = None,
        filial_abbr: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> Tuple[Sequence[Group], int]:
        query = select(self.model)

        if abbr:
            query = query.where(self.model.abbr.ilike(f"%{abbr}%"))

        if course_abbr:
            query = query.join(self.model.course).where(
                Course.abbr.ilike(f"%{course_abbr}%"),
            )

        # todo other joins
        if department_abbr or faculty_abbr or filial_abbr:
            msg = "Department, faculty and filial filters are not implemented"
            raise NotImplementedError(msg)

        count_query = select(count()).select_from(query.subquery())
        total = await session.scalar(count_query)

        query = (
            query.order_by(self.model.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await session.execute(query)
        groups = result.scalars().all()

        return groups, total or 0

    async def get_schedule_by_group_id(
        self,
        session: AsyncSession,
        group_id: int,
        dt_from: datetime,
        dt_to: datetime,
    ) -> Optional[GroupScheduleResult]:
        group_query = select(self.model).where(self.model.id == group_id)
        group_result = await session.execute(group_query)
        group = group_result.scalars().first()

        if not group:
            return None

        pairs_query = (
            select(SchedulePair)
            .options(
                joinedload(SchedulePair.teachers),
                joinedload(SchedulePair.audiences),
                joinedload(SchedulePair.discipline),
            )
            .join(
                schedule_pair_group,
                SchedulePair.id == schedule_pair_group.c.schedule_pair_id,
            )
            .where(
                schedule_pair_group.c.group_id == group_id,
            )
        )

        result = await session.execute(pairs_query)
        schedule_pairs = result.unique().scalars().all()

        concrete_pairs = _generate_concrete_pairs(
            schedule_pairs=schedule_pairs,
            dt_from=dt_from,
            dt_to=dt_to,
        )

        return GroupScheduleResult(
            group=GroupBase(
                id=group.id,
                abbr=group.abbr,
                course_id=group.course_id,
                semester_num=group.semester_num,
            ),
            schedule_pairs=concrete_pairs,
        )


@lru_cache(maxsize=1)
def group_repo() -> GroupRepo:
    return GroupRepo()
