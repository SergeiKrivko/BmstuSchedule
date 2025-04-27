from functools import lru_cache

from app.models.audience import Audience
from app.repos.base_repo import UniqueFieldRepo


class AudienceRepo(UniqueFieldRepo[Audience]):
    model = Audience


@lru_cache(maxsize=1)
def audience_repo() -> AudienceRepo:
    return AudienceRepo()
