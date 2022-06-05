from functools import wraps
from typing import cast

from ariadne_graphql_modules import ObjectType
from graphql import GraphQLSchema, GraphQLObjectType

from .errors import AuthenticationGraphQLError, ForbiddenGraphQLError


class AdminQueries(ObjectType):
    __abstract__ = True

    @classmethod
    def __bind_to_schema__(cls, schema: GraphQLSchema):
        graphql_type = cast(GraphQLObjectType, schema.type_map.get(cls.graphql_name))

        for field_name, field_resolver in cls.resolvers.items():
            secured_resolver = secure_resolver(field_resolver)
            graphql_type.fields[field_name].resolve = secured_resolver


def secure_resolver(f):
    @wraps(f)
    def admin_resolver(obj, info, **kwargs):
        user = info.context["user"]
        if not user:
            raise AuthenticationGraphQLError()
        if not user.is_admin:
            raise ForbiddenGraphQLError()

        return f(obj, info, **kwargs)

    return admin_resolver