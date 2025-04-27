from functools import lru_cache

from app.models.schedule_pair import SchedulePair
from app.repos.base_repo import UniqueFieldRepo


class SchedulePairRepo(UniqueFieldRepo[SchedulePair]):
    model = SchedulePair


@lru_cache(maxsize=1)
def schedule_pair_repo() -> SchedulePairRepo:
    return SchedulePairRepo()
