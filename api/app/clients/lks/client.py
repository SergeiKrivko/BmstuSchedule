from functools import lru_cache
from typing import Any
from uuid import UUID

import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

from app.clients.lks.models import (
    Node,
    Schedule,
    ScheduleResponseBody,
    StructureResponseBody,
)
from app.settings import LksSettings, lks_settings


class LksClient:
    def __init__(self, settings: LksSettings) -> None:
        self.__base_url = settings.base_api_url
        self.__use_ssl = settings.use_ssl

    def __get_session(self) -> aiohttp.ClientSession:
        connector = aiohttp.TCPConnector(ssl=self.__use_ssl)
        return aiohttp.ClientSession(
            base_url=self.__base_url,
            connector=connector,
            raise_for_status=True,
        )

    async def _get(self, url: str) -> dict[str, Any]:
        async with self.__get_session() as session, session.get(url) as response:
            return await response.json()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def get_structure(self) -> Node:
        data = await self._get("structure")
        response = StructureResponseBody.model_validate(data)
        return response.data

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def get_schedule(self, group_id: UUID) -> Schedule:
        data = await self._get(f"schedules/groups/{group_id}/public")
        response = ScheduleResponseBody.model_validate(data)
        return response.data


@lru_cache(maxsize=1)
def get_lks_client() -> LksClient:
    settings = lks_settings()

    return LksClient(settings=settings)
