from functools import lru_cache

from app.models.department import Department
from app.repos.base_repo import LksIdRepo


class DepartmentRepo(LksIdRepo[Department]):
    model = Department


@lru_cache(maxsize=1)
def department_repo() -> DepartmentRepo:
    return DepartmentRepo()
