from datetime import datetime, timedelta
from functools import lru_cache
from typing import Annotated, Sequence

from aiocache import cached
from fastapi import Depends

from app import domain
from app.api import schemas
from app.clients import lks
from app.core.schedule_manager.helpers import create_concrete_pair
from app.settings import schedule_manager_settings


class ScheduleManager:
    def __init__(self, lks_client: lks.LksClient) -> None:
        self.lks_client = lks_client

    async def generate_concrete_pairs(
        self,
        schedule_pairs: Sequence[domain.SchedulePair],
        dt_from: datetime,
        dt_to: datetime,
    ) -> list[schemas.SchedulePairRead]:
        concrete_pairs = []
        current_date = dt_from.replace(hour=0, minute=0, second=0, microsecond=0)

        while current_date <= dt_to:
            concrete_pairs.extend(
                await self._generate_concrete_pairs_for_date(
                    schedule_pairs,
                    current_date,
                    dt_from,
                    dt_to,
                ),
            )
            current_date += timedelta(days=1)
        return concrete_pairs

    async def _generate_concrete_pairs_for_date(
        self,
        schedule_pairs: Sequence[domain.SchedulePair],
        current_date: datetime,
        dt_from: datetime,
        dt_to: datetime,
    ) -> list[schemas.SchedulePairRead]:
        current_week = await self.current_week()
        week = domain.Week.from_datetime(current_date, current_week)
        day_of_week = domain.DayOfWeek.from_datetime(current_date)

        return self.create_concrete_pairs_for_day_and_week(
            schedule_pairs=schedule_pairs,
            day_of_week=day_of_week,
            week=week,
            current_date=current_date,
            dt_from=dt_from,
            dt_to=dt_to,
        )

    @classmethod
    def create_concrete_pairs_for_day_and_week(
        cls,
        schedule_pairs: Sequence[domain.SchedulePair],
        day_of_week: domain.DayOfWeek,
        week: domain.Week,
        current_date: datetime,
        dt_from: datetime,
        dt_to: datetime,
    ) -> list[schemas.SchedulePairRead]:
        concrete_pairs = []
        for pair in schedule_pairs:
            if not cls.is_pair_matching_day_and_week(pair, day_of_week, week):
                continue

            concrete_times = domain.TimeSlot.from_str_times(
                start_time=pair.start_time,
                end_time=pair.end_time,
                current_date=current_date,
            )

            if not concrete_times.is_in_range(dt_from, dt_to):
                continue

            concrete_pair = create_concrete_pair(pair, concrete_times)
            concrete_pairs.append(concrete_pair)

        return concrete_pairs

    @staticmethod
    def is_pair_matching_day_and_week(
        pair: domain.SchedulePair,
        day_of_week: domain.DayOfWeek,
        week: domain.Week,
    ) -> bool:
        return domain.DayOfWeek(pair.day) == day_of_week and domain.Week(
            pair.week,
        ).match(week)

    @cached(ttl=schedule_manager_settings().current_schedule_cache_ttl_sec)
    async def current_schedule(self) -> lks.CurrentSchedule:
        return await self.lks_client.get_current_schedule()

    async def current_week(self) -> domain.Week:
        current_schedule = await self.current_schedule()
        return domain.Week.from_lks_ru(current_schedule.week_ru)


@lru_cache
def schedule_manager() -> ScheduleManager:
    return ScheduleManager(lks_client=lks.get_lks_client())


ScheduleManagerDep = Annotated[ScheduleManager, Depends(schedule_manager)]
