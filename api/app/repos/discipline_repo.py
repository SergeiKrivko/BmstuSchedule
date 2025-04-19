from functools import lru_cache

from app.models.discipline import Discipline
from app.repos.base_repo import BaseRepo


class DisciplineRepo(BaseRepo[Discipline]):
    model = Discipline


@lru_cache(maxsize=1)
def discipline_repo() -> DisciplineRepo:
    return DisciplineRepo()
