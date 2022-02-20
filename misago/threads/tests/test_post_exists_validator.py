import pytest

from ...categories.models import CategoryType
from ..errors import PostNotFoundError
from ..validators import PostExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_post_if_id_given_exists_in_db(context, post):
    validator = PostExistsValidator(context)
    assert await validator(post.id) == post


@pytest.mark.asyncio
async def test_validator_raises_post_not_exists_error_if_post_not_exists(context):
    validator = PostExistsValidator(context)
    with pytest.raises(PostNotFoundError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_returns_post_if_given_id_and_type_exists_in_db(context, post):
    validator = PostExistsValidator(context, CategoryType.THREADS)
    assert await validator(post.id) == post


@pytest.mark.asyncio
async def test_validator_raises_post_not_exists_error_for_wrong_category_type(
    context, post
):
    validator = PostExistsValidator(context, CategoryType.PRIVATE_THREADS)
    with pytest.raises(PostNotFoundError):
        await validator(post.id)