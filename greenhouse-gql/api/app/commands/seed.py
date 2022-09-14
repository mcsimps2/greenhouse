import click
from flask.cli import with_appcontext
from flask_bcrypt import generate_password_hash

from app import models


def _seed():
    acc = models.UserAccount(
        id="5ec62eaf-d3f6-454d-a444-3ed272cb1735",
        email="mcsimps2@gmail.com",
        password=generate_password_hash("pwd").decode("utf-8"),
        first_name="Matt",
        last_name="Simpson",
    )
    models.db.session.add(acc)
    models.db.session.flush()
    greenhouse = models.Greenhouse(
        id="7c355b69-e412-47a2-a0dd-b20449e04a29",
        name="Bedroom",
        services=[
            models.Service(
                name="Lights",
            ),
            models.Service(
                name="Fan",
            ),
            models.Service(
                name="Humidifier",
            ),
            models.Service(
                name="Thermometer",
            ),
        ]
    )
    models.db.session.add(greenhouse)
    models.db.session.flush()
    models.db.session.add(
        models.AccountGreenhouseRole(
            account=acc,
            greenhouse=greenhouse,
            role=models.Role.MANAGER
        )
    )
    models.db.session.commit()


@click.command()
@with_appcontext
def seed():
    _seed()
