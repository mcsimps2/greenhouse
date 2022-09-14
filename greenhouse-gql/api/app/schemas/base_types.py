import logging
from functools import wraps

import graphene

from app import errors


logger = logging.getLogger(__name__)


def catch_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.ApiError:
            # Users are allowed to see these messages
            raise
        except Exception as e:
            logger.exception("An unknown error occurred.")
            # Unknown errors (e.g. some weird postgres error). Message may contain
            # sensitive data (e.g. table schemas) and should be hidden from users
            raise errors.ApiError(
                "An error occurred. Please try again or contact support."
            ) from e

    return wrapper


# Solutions - https://github.com/graphql-python/graphene/issues/902, https://github.com/graphql-python/graphene/issues/1368
class SchemaObjectType(graphene.ObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        interfaces=(),
        possible_types=(),
        default_resolver=None,
        _meta=None,
        **options,
    ):
        # This works out of the box on mutations
        # To make it work with queries, need to explicitly use graphene.Field(..., resolver=...)
        super().__init_subclass_with_meta__(
            interfaces, possible_types, default_resolver, _meta, **options
        )
        for f in cls._meta.fields:
            field = getattr(cls, f)
            if hasattr(field, "resolver"):
                field.resolver = (
                    catch_errors(field.resolver) if field.resolver else field.resolver
                )
