from functools import lru_cache

from app.models.university import University
from app.repos.base_repo import BaseRepo


class UniversityRepo(BaseRepo[University]):
    model = University


@lru_cache(maxsize=1)
def university_repo() -> UniversityRepo:
    return UniversityRepo()
