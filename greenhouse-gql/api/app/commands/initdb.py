import click
from flask.cli import with_appcontext
from flask_migrate import upgrade

from .seed import _seed


@click.command()
@with_appcontext
def initdb():
    upgrade()
    _seed()
