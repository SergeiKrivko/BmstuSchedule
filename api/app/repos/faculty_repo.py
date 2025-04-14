from functools import lru_cache

from app.models.faculty import Faculty
from app.repos.base_repo import BaseRepo


class FacultyRepo(BaseRepo[Faculty]):
    model = Faculty


@lru_cache(maxsize=1)
def faculty_repo() -> FacultyRepo:
    return FacultyRepo()
