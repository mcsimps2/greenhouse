from functools import wraps

from sqlalchemy.orm.exc import NoResultFound
from flask import current_app
from flask_jwt_extended import (
    JWTManager,
    verify_jwt_in_request,
    get_current_user,
    get_jwt,
)
from flask_jwt_extended.exceptions import NoAuthorizationError, UserLookupError

from app.models import db, Account
from app.util.choices import StrChoices

jwt_manager = JWTManager()


class HasuraClaim(StrChoices):
    DEFAULT_ROLE = "x-hasura-default-role"
    ALLOWED_ROLES = "x-hasura-allowed-roles"
    ACCOUNT_ID = "x-hasura-account-id"


class HasuraRole(StrChoices):
    ADMIN = "admin"
    ANON = "anonymous"
    CLIENT = "client"


class GreenhouseClaim(StrChoices):
    ACCOUNT_TYPE = "x-account-type"
    SUPERUSER = "x-superuser"


HASURA_NAMESPACE_JWT_CLAIM = "hasura"
GREENHOUSE_NAMESPACE_JWT_CLAIM = "greenhouse"
JWT_SUBJECT_FIELD = "sub"


@jwt_manager.user_identity_loader
def account_identity_lookup(account):
    if account is None:
        # Hasura requires a string instead of null for anonymous users
        return ""
    return account.id


@jwt_manager.user_lookup_loader
def retrieve_account_from_identity(_, jwt_data):
    identity = jwt_data[JWT_SUBJECT_FIELD]
    if identity == "":
        return None
    try:
        return (
            db.session.query(Account)
            # pylint: disable=singleton-comparison
            .filter(db.and_(Account.id == identity, Account.active == True)).one()
        )
    except (NoResultFound, ValueError):
        # Account has been deactivated
        # Do not raise an error, but return None
        # Will raise UserLookupError when verify_jwt_in_request called
        # https://flask-jwt-extended.readthedocs.io/en/stable/api/
        # The decorated function can return any python object, which can then be accessed in a protected endpoint. If an object cannot be loaded, for example if a user has been deleted from your database, None must be returned to indicate that an error occurred loading the user.
        return None


def get_current_account():
    try:
        return get_current_user()
    except UserLookupError:
        return None


def jwt_protected(
    optional=False,
    fresh=False,
    refresh=False,
    locations=None,
    account_type=None,
    superuser=None,
):
    """
    Same as the jwt_required function but does not allow anonymous users (null identity). Note that this
    exists because Hasura requires JWTs for anonymous users.
    """

    def protected_route_decorator(fn):
        @wraps(fn)
        def verify_auth(*args, **kwargs):
            try:
                # Will raise UserLookupError if anonymous JWT
                verify_jwt_in_request(optional, fresh, refresh, locations)
            except UserLookupError as e:
                raise NoAuthorizationError("Anonymous user forbidden.") from e

            claims = get_jwt()
            if not claims[JWT_SUBJECT_FIELD]:
                # Anonymous user
                raise NoAuthorizationError("Anonymous user forbidden.")

            if (
                account_type
                and claims[GREENHOUSE_NAMESPACE_JWT_CLAIM][GreenhouseClaim.ACCOUNT_TYPE]
                != account_type
            ):
                raise NoAuthorizationError("Account is not of an allowed type.")
            if superuser and not claims[GREENHOUSE_NAMESPACE_JWT_CLAIM].get(
                GreenhouseClaim.SUPERUSER, False
            ):
                raise NoAuthorizationError("Account is not superuser.")
            # Compatibility with flask < 2.0
            if hasattr(current_app, "ensure_sync") and callable(
                getattr(current_app, "ensure_sync", None)
            ):
                return current_app.ensure_sync(fn)(*args, **kwargs)

            return fn(*args, **kwargs)

        return verify_auth

    return protected_route_decorator
