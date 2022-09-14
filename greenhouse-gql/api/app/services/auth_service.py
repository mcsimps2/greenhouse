from flask_bcrypt import check_password_hash
from flask_jwt_extended import (
    create_access_token,
)
from sqlalchemy.exc import NoResultFound

from app import models
from app.errors import Unauthorized
from app.middleware.jwt import (
    GREENHOUSE_NAMESPACE_JWT_CLAIM,
    GreenhouseClaim,
    HasuraClaim,
    HasuraRole,
    HASURA_NAMESPACE_JWT_CLAIM,
)
from app.models import Account, AccountType, db


def create_hasura_claims(account_id: str, default_role: str, allowed_roles: list):
    hasura_claims = {
        HasuraClaim.ALLOWED_ROLES: allowed_roles,
        HasuraClaim.DEFAULT_ROLE: default_role,
    }
    if account_id is not None:
        hasura_claims[HasuraClaim.ACCOUNT_ID] = account_id
    total_claims = {HASURA_NAMESPACE_JWT_CLAIM: hasura_claims}
    return total_claims


def create_hasura_claims_for_account(account):
    allowed_roles = [HasuraRole.CLIENT, HasuraRole.ANON]
    if account.superuser:
        allowed_roles.append(HasuraRole.ADMIN)
    return create_hasura_claims(account.id, HasuraRole.CLIENT, allowed_roles)


def create_access_token_for_account(account: Account):
    return create_access_token(
        account,
        additional_claims={
            GREENHOUSE_NAMESPACE_JWT_CLAIM: {
                GreenhouseClaim.ACCOUNT_TYPE: account.type,
                GreenhouseClaim.SUPERUSER: account.superuser,
            },
            **create_hasura_claims_for_account(account),
        },
    )


def create_user_token(email: str, password: str) -> tuple:
    try:
        user = models.UserAccount.query.filter(
            db.and_(
                models.UserAccount.email == email.lower(),
                models.UserAccount.active == True,
            )
        ).one()
    except NoResultFound as e:
        raise Unauthorized("Invalid login credentials") from e

    if user and check_password_hash(user.password, password):
        return create_access_token_for_account(user)

    raise Unauthorized("Invalid login credentials")


def create_sa_token(sa_id: str) -> tuple:
    try:
        acc = models.ServiceAccount.query.filter(
            db.and_(
                models.ServiceAccount.id == service_account_id,
                models.ServiceAccount.active == True,
            )
        ).one()
    except NoResultFound as e:
        raise Unauthorized("Invalid service account") from e

    return create_access_token_for_account(acc)


def create_anonymous_access_token() -> tuple:
    access = create_access_token(
        None,
        additional_claims={
            GREENHOUSE_NAMESPACE_JWT_CLAIM: {
                GreenhouseClaim.ACCOUNT_TYPE: AccountType.USER,
                GreenhouseClaim.SUPERUSER: False,
            },
            **create_hasura_claims(None, HasuraRole.ANON, [HasuraRole.ANON]),
        },
    )
    return access
