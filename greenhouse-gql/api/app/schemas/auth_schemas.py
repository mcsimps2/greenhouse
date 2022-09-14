import graphene

from app.middleware.jwt import jwt_protected
from app.services import auth_service


class LogInAnonymous(graphene.Mutation):
    class Arguments:
        pass

    access_token = graphene.String()

    @staticmethod
    # pylint: disable=unused-argument
    def mutate(root, info):
        access = auth_service.create_anonymous_access_token()
        return LogInAnonymous(access)


class LogInUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    access_token = graphene.String()

    @staticmethod
    # pylint: disable=unused-argument
    def mutate(root, info, email, password):
        access = auth_service.create_user_token(email, password)
        return LogInUser(access_token=access)


class CreateSAToken(graphene.Mutation):
    class Arguments:
        sa_id = graphene.String(required=True)

    access_token = graphene.String()

    @staticmethod
    @jwt_protected(superuser=True)
    # pylint: disable=unused-argument
    def mutate(root, info, sa_id):
        access = auth_service.create_sa_token(sa_id)
        return CreateSAToken(access_token=access)
