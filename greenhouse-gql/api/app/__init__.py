import logging
import sys

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_graphql import GraphQLView


bcrypt = Bcrypt()
cors = CORS()


def initialize_extensions(app):
    # pylint: disable=import-outside-toplevel
    from app.models import db, migrate
    from app.middleware.jwt import jwt_manager

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)
    cors.init_app(app)


def register_graphql(app):
    # pylint: disable=import-outside-toplevel
    from app.schemas import schema

    app.add_url_rule(
        "/v1/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=False),
    )


def register_blueprints(app):
    pass


# pylint: disable=unused-argument
def register_middleware(app):
    pass


# pylint: disable=unused-argument
def register_error_handlers(app):
    pass


def register_commands(app):
    # pylint: disable=import-outside-toplevel
    from app.commands import commands

    for command in commands:
        app.cli.add_command(command)


def initialize_logging(app):
    # Instantiates a client
    logging.basicConfig(
        stream=sys.stdout,
        format="%(levelname)s %(asctime)s - %(message)s",
        level=logging.DEBUG,
    )
    logging.info("Logging successfully configured")


def create_app(
    config_filename=None, config_object=None, relative_config_path=False, **kwargs
):
    if relative_config_path:
        app = Flask(__name__, instance_relative_config=True)
    else:
        app = Flask(__name__)

    if config_filename:
        app.config.from_pyfile(config_filename)
    elif config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object("config")

    # Apply any keyword updates
    if kwargs:
        app.config.update(kwargs)

    app.url_map.strict_slashes = False

    initialize_logging(app)
    initialize_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_middleware(app)
    register_commands(app)
    register_graphql(app)

    return app
