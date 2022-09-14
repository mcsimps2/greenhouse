import graphene

from .base_types import SchemaObjectType
from . import (
    auth_schemas,
)


class Mutation(SchemaObjectType):
    log_in_anonymous = auth_schemas.LogInAnonymous.Field()
    log_in_user = auth_schemas.LogInUser.Field()
    create_sa_token = auth_schemas.CreateSAToken.Field()


class Query(SchemaObjectType):
    hello = graphene.String(default_value="Hi!")


class Subscription(SchemaObjectType):
    hello = graphene.String(default_value="Hi!")


schema = graphene.Schema(
    query=Query, mutation=Mutation, subscription=Subscription, auto_camelcase=False
)
