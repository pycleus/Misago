import pytest

from ....tables import users, user_groups
from ....users.models import User, UserGroup
from ..exceptions import (
    DoesNotExist,
    InvalidColumnError,
    MultipleObjectsReturned,
)
from ..registry import MapperRegistry

mapper_registry = MapperRegistry()
mapper_registry.set_mapping(users, User)
mapper_registry.set_mapping(user_groups, UserGroup)


@pytest.mark.asyncio
async def test_one_object_can_be_retrieved(user):
    assert await mapper_registry.query_table(users).one() == user


@pytest.mark.asyncio
async def test_one_object_can_be_retrieved_by_selector(user, admin):
    assert await mapper_registry.query_table(users).one(email=admin.email) == admin


@pytest.mark.asyncio
async def test_one_object_can_be_retrieved_by_filter(user, admin):
    assert (
        await mapper_registry.query_table(users).filter(email=admin.email).one()
        == admin
    )


@pytest.mark.asyncio
async def test_one_object_can_be_retrieved_by_exclude(user, admin):
    assert (
        await mapper_registry.query_table(users).exclude(email=admin.email).one()
        == user
    )


@pytest.mark.asyncio
async def test_one_object_can_be_retrieved_as_named_tuple(user):
    result = await mapper_registry.query_table(users).one("id", "email", named=True)
    assert result.id == user.id
    assert result.email == user.email
    assert result == (user.id, user.email)


@pytest.mark.asyncio
async def test_one_object_can_be_retrieved_as_tuple(user):
    result = await mapper_registry.query_table(users).one("id", "email")
    assert result == (user.id, user.email)


@pytest.mark.asyncio
async def test_one_object_can_be_retrieved_as_single_value(user):
    result = await mapper_registry.query_table(users).one_flat("email")
    assert result == user.email


@pytest.mark.asyncio
async def test_error_is_raised_if_column_name_is_invalid(user):
    with pytest.raises(InvalidColumnError):
        await mapper_registry.query_table(users).one("id", "invalid", "email")


@pytest.mark.asyncio
async def test_one_object_query_raises_error_on_multiple_results(user, admin):
    with pytest.raises(MultipleObjectsReturned):
        await mapper_registry.query_table(users).one()


@pytest.mark.asyncio
async def test_one_object_query_raises_error_on_no_results(db):
    with pytest.raises(DoesNotExist):
        await mapper_registry.query_table(users).one()