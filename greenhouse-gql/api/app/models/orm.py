"""
https://docs.sqlalchemy.org/en/14/orm/contextual.html#using-thread-local-scope-with-web-applications

How SQLAclhemy + Flask work together

db.session is a ScopedSession, which acts as a registry and thread-local proxy to Session
Not all methods are available, so to get the real session for the calling thread, you can just use the __call__ method.
e.g. db.session().in_transaction() since db.session.in_transaction() raises an AttributeError

statement_a (e.g. a query, such as get_current_account) -> BEGIN (implicit)
statement_b, raise exc (e.g. an insert)
(Flask) returns response
(Flask) Session.close -> Issues ROLLBACK by default

This means we don't really need to use context managers like so
with session.begin():
    # this will automatically commit at end or rollback if error
    ...
# https://docs.sqlalchemy.org/en/14/orm/session_transaction.html
"The Session itself features a Session.close() method.
If the Session is begun within a transaction that has not yet been committed or rolled back, this method will
cancel (i.e. rollback) that transaction, and also expunge all objects contained within the Session object’s state.
If the Session is being used in such a way that a call to Session.commit() or Session.rollback() is not guaranteed
(e.g. not within a context manager or similar), the close method may be used to ensure all resources are released."
"""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID

SQLACLHEMY_NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=SQLACLHEMY_NAMING_CONVENTION))
migrate = Migrate()


class UUIDMixin:
    id = db.Column(
        UUID(), primary_key=True, server_default=db.text("uuid_generate_v4()")
    )


class IdMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class CreatedAtMixin:
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
