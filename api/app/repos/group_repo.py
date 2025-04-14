from functools import lru_cache

from app.models.group import Group
from app.repos.base_repo import BaseRepo


class GroupRepo(BaseRepo[Group]):
    model = Group


@lru_cache(maxsize=1)
def group_repo() -> GroupRepo:
    return GroupRepo()
