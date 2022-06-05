# `thread_create_hook`

```python
from misago.graphql.thread.hooks.threadcreate import thread_create_hook

thread_create_hook.call_action(
    action: ThreadCreateAction,
    context: Context,
    cleaned_data: ThreadCreateInput,
)
```

A filter for the function used by `threadCreate` GraphQL mutation to create new thread in the database.

Returns tuple of `Thread` and `Post` dataclasses with newly created thread data and `ParsedMarkupMetadata` being Python `dict` with metadata for parsed message.


## Required arguments

### `action`

```python
async def thread_create(
    context: Context,
    cleaned_data: ThreadCreateInput,
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    ...
```

Next filter or built-in function used to create new thread in the database.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `category`, `title` and `markup` keys and optionally `is_closed` key:

```python
class ThreadCreateInput(TypedDict):
    category: Category
    title: str
    markup: str
    is_closed: Optional[bool]
```