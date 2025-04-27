from functools import lru_cache

from app.models.course import Course
from app.repos.base_repo import UniqueFieldRepo


class CourseRepo(UniqueFieldRepo[Course]):
    model = Course


@lru_cache(maxsize=1)
def course_repo() -> CourseRepo:
    return CourseRepo()
