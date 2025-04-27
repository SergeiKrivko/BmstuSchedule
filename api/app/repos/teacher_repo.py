from functools import lru_cache

from app.models.teacher import Teacher
from app.repos.base_repo import LksIdRepo


class TeacherRepo(LksIdRepo[Teacher]):
    model = Teacher


@lru_cache(maxsize=1)
def teacher_repo() -> TeacherRepo:
    return TeacherRepo()
