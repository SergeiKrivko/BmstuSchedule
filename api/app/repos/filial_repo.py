from functools import lru_cache

from app.models.filial import Filial
from app.repos.base_repo import BaseRepo


class FilialRepo(BaseRepo[Filial]):
    model = Filial


@lru_cache(maxsize=1)
def filial_repo() -> FilialRepo:
    return FilialRepo()
