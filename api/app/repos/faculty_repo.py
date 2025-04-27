from functools import lru_cache

from app.models.faculty import Faculty
from app.repos.base_repo import LksIdRepo


class FacultyRepo(LksIdRepo[Faculty]):
    model = Faculty


@lru_cache(maxsize=1)
def faculty_repo() -> FacultyRepo:
    return FacultyRepo()
