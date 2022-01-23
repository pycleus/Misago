from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....errors import ErrorsList
from ....loaders import load_thread, store_thread
from ....threads.models import Thread
from ....threads.move import move_thread
from ....validation import (
    CategoryExistsValidator,
    CategoryIsOpenValidator,
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    UserIsAuthorizedRootValidator,
    Validator,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadmove import ThreadMoveInput, thread_move_hook, thread_move_input_hook

thread_move_mutation = MutationType()


@thread_move_mutation.field("threadMove")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_thread_move(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model()
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await load_thread(info.context, cleaned_data["thread"])
    else:
        thread = None

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            "category": [
                CategoryExistsValidator(info.context),
                CategoryIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await thread_move_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread, "updated": False}

    updated_thread = await thread_move_hook.call_action(
        thread_move_action, info.context, cleaned_data
    )

    return {"thread": updated_thread, "updated": updated_thread != thread}


def create_input_model() -> Type[BaseModel]:
    return create_model(
        "ThreadMoveInputModel",
        thread=(PositiveInt, ...),
        category=(PositiveInt, ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadMoveInput,
    errors: ErrorsList,
) -> Tuple[ThreadMoveInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_move_action(
    context: GraphQLContext, cleaned_data: ThreadMoveInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread = await move_thread(thread, cleaned_data["category"])

    store_thread(context, thread)

    return thread