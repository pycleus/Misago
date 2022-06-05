from typing import Awaitable, Optional, cast

from ariadne_graphql_modules import DeferredType, ObjectType, gql
from graphql import GraphQLResolveInfo

from ...categories.loaders import categories_loader
from ...categories.models import Category
from ...threads.loaders import posts_loader
from ...threads.models import Post, Thread
from ...users.loaders import users_loader
from ...users.models import User
from ..args import clean_id_arg, handle_invalid_args
from ..post import PostType
from ..scalars import DateTimeScalar, GenericScalar


class ThreadType(ObjectType):
    __schema__ = gql(
        """
        type Thread {
            id: ID!
            category: Category!
            firstPost: Post
            starter: User
            starterName: String!
            lastPost: Post
            lastPoster: User
            lastPosterName: String!
            title: String!
            slug: String!
            startedAt: DateTime!
            lastPostedAt: DateTime!
            replies: Int!
            post(id: ID!): Post
            isClosed: Boolean!
            extra: Generic!
        }
        """
    )
    __aliases__ = {
        "firstPost": "first_post",
        "starterName": "starter_name",
        "lastPost": "last_post",
        "lastPoster": "last_poster",
        "lastPosterName": "last_poster_name",
        "startedAt": "started_at",
        "lastPostedAt": "last_posted_at",
        "isClosed": "is_closed",
    }
    __requires__ = [
        DeferredType("Category"),
        DeferredType("User"),
        DateTimeScalar,
        GenericScalar,
        PostType,
    ]

    @staticmethod
    def resolve_category(obj: Thread, info: GraphQLResolveInfo) -> Awaitable[Category]:
        category = categories_loader.load(info.context, obj.category_id)
        return cast(Awaitable[Category], category)

    @staticmethod
    def resolve_first_post(
        obj: Thread, info: GraphQLResolveInfo
    ) -> Optional[Awaitable[Optional[Post]]]:
        if obj.first_post_id:
            return posts_loader.load(info.context, obj.first_post_id)
        return None

    @staticmethod
    async def resolve_starter(obj: Thread, info: GraphQLResolveInfo) -> Optional[User]:
        if obj.starter_id:
            starter = await users_loader.load(info.context, obj.starter_id)
            if starter and starter.is_active:
                return starter
        return None

    @staticmethod
    def resolve_last_post(
        obj: Thread, info: GraphQLResolveInfo
    ) -> Optional[Awaitable[Optional[Post]]]:
        if obj.last_post_id:
            return posts_loader.load(info.context, obj.last_post_id)
        return None

    @staticmethod
    async def resolve_last_poster(
        obj: Thread, info: GraphQLResolveInfo
    ) -> Optional[User]:
        if obj.last_poster_id:
            last_poster = await users_loader.load(info.context, obj.last_poster_id)
            if last_poster and last_poster.is_active:
                return last_poster
        return None

    @staticmethod
    @handle_invalid_args
    async def resolve_post(
        obj: Thread,
        info: GraphQLResolveInfo,
        *,
        id: str,  # pylint: disable=redefined-builtin
    ) -> Optional[Post]:
        post_id = clean_id_arg(id)
        post = await posts_loader.load(info.context, post_id)
        if post and post.thread_id == obj.id:
            return post
        return None