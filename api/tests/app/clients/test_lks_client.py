import uuid

import pytest
from aioresponses import aioresponses

from app.clients.lks.client import LksClient, get_lks_client
from app.clients.lks.models import Schedule, StructureNode

pytestmark = pytest.mark.asyncio


@pytest.fixture(name="lks_client")
def lks_client_fixture() -> LksClient:
    return get_lks_client()


async def test_get_structure(lks_client: LksClient) -> None:
    structure_id = uuid.uuid4()

    mocked_response = {
        "data": {
            "uuid": str(structure_id),
            "abbr": "RootAbbr",
            "name": "Root Node",
            "nodeType": "root",
            "children": [],
        },
    }
    with aioresponses() as mock:
        mock.get(
            "https://lks.bmstu.ru/lks-back/api/v1/structure",
            payload=mocked_response,
        )

        structure: StructureNode = await lks_client.get_structure()

        assert structure.id == structure_id
        assert structure.abbr == "RootAbbr"
        assert structure.name == "Root Node"
        assert structure.type == "root"
        assert structure.children == []


async def test_get_schedule(lks_client: LksClient) -> None:
    group_id = uuid.uuid4()

    mocked_response = {
        "data": {
            "uuid": str(group_id),
            "title": "Sample Schedule",
            "schedule": [
                {
                    "groups": [{"uuid": str(uuid.uuid4()), "name": "IU7-65"}],
                    "audiences": [{"uuid": str(uuid.uuid4()), "name": "101"}],
                    "teachers": [
                        {
                            "uuid": str(uuid.uuid4()),
                            "firstName": "Наталья",
                            "middleName": "Юрьевна",
                            "lastName": "Рязанова",
                        },
                    ],
                    "discipline": {
                        "uuid": str(uuid.uuid4()),
                        "abbr": "ВУЦ",
                        "fullName": "ВУЦ",
                        "shortName": "ВУЦ",
                        "actType": "seminar",
                    },
                    "day": 1,
                    "week": "ch",
                    "startTime": "09:00",
                    "endTime": "10:30",
                },
            ],
        },
    }

    with aioresponses() as mock:
        mock.get(
            f"https://lks.bmstu.ru/lks-back/api/v1/schedules/groups/{group_id}/public",
            payload=mocked_response,
        )

        schedule: Schedule = await lks_client.get_schedule(group_id)

        assert schedule.id == group_id
        assert schedule.title == "Sample Schedule"
        assert len(schedule.data) == 1

        pair = schedule.data[0]
        assert pair.day == 1
        assert pair.start_time == "09:00"
        assert pair.end_time == "10:30"
        assert pair.discipline.abbr == "ВУЦ"
