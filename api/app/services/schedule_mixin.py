from datetime import datetime

from app.api.schemas.schedule_pair import SchedulePairRead
from app.core.schedule_manager.manager import ScheduleManager
from app.domain import schedule


class ScheduleMixin:
    def __init__(self, schedule_manager: ScheduleManager) -> None:
        self._schedule_manager = schedule_manager

    async def _generate_concrete_pairs(
        self,
        schedule_result: schedule.ScheduleResult[schedule.T],
        dt_from: datetime,
        dt_to: datetime,
    ) -> list[SchedulePairRead]:
        return await self._schedule_manager.generate_concrete_pairs(
            schedule_pairs=schedule_result.pairs,
            dt_from=dt_from,
            dt_to=dt_to,
        )
