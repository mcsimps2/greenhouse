import click
from flask.cli import with_appcontext

from app.services import auth_service


def _anontoken():
    return auth_service.create_anonymous_access_token()


@click.command()
@with_appcontext
def anontoken():
    print(_anontoken())
