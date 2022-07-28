from typing import List

import pytest

from ...tables import attachment_types
from ..objectmapper2 import ObjectMapper

mapper = ObjectMapper()
root_query = mapper.query_table(attachment_types)


async def consume_generator(generator) -> List[str]:
    results: List[str] = []
    async for result in generator:
        results.append(result["name"])
    return results


@pytest.mark.asyncio
async def test_empty_table_can_be_batched(db):
    await root_query.delete_all()

    results = await consume_generator(root_query.batch())
    assert results == []


@pytest.mark.asyncio
async def test_small_table_can_be_batched(db):
    await root_query.delete_all()

    items = []
    for i in range(1, 6):
        items.append(
            await root_query.insert(
                {
                    "name": f"#{i}",
                    "extensions": [],
                    "mimetypes": [],
                    "size_limit": None,
                    "is_active": True,
                },
            )
        )

    results = await consume_generator(root_query.batch())
    assert results == ["#5", "#4", "#3", "#2", "#1"]


@pytest.mark.asyncio
async def test_small_table_can_be_batched_in_ascending_order(db):
    await root_query.delete_all()

    items = []
    for i in range(1, 6):
        items.append(
            await root_query.insert(
                {
                    "name": f"#{i}",
                    "extensions": [],
                    "mimetypes": [],
                    "size_limit": None,
                    "is_active": True,
                },
            )
        )

    results = await consume_generator(root_query.batch(ascending=True))
    assert results == ["#1", "#2", "#3", "#4", "#5"]


@pytest.mark.asyncio
async def test_large_table_can_be_batched(db):
    await root_query.delete_all()

    items = []
    for i in range(1, 41):
        items.append(
            await root_query.insert(
                {
                    "name": f"#{i}",
                    "extensions": [],
                    "mimetypes": [],
                    "size_limit": None,
                    "is_active": True,
                },
            )
        )

    results = await consume_generator(root_query.batch())
    assert results == [f"#{i}" for i in reversed(range(1, 41))]


@pytest.mark.asyncio
async def test_large_table_can_be_batched_in_ascending_order(db):
    await root_query.delete_all()

    items = []
    for i in range(1, 41):
        items.append(
            await root_query.insert(
                {
                    "name": f"#{i}",
                    "extensions": [],
                    "mimetypes": [],
                    "size_limit": None,
                    "is_active": True,
                },
            )
        )

    results = await consume_generator(root_query.batch(ascending=True))
    assert results == [f"#{i}" for i in range(1, 41)]
