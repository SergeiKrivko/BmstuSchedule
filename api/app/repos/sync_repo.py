from functools import lru_cache

from app.models.synchronization import Synchronization
from app.repos.base_repo import BaseRepo


class SyncRepo(BaseRepo[Synchronization]):
    model = Synchronization


@lru_cache(maxsize=1)
def sync_repo() -> SyncRepo:
    return SyncRepo()
