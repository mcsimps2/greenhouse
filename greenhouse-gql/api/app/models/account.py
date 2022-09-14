from app.util.choices import StrChoices

from .orm import CreatedAtMixin, UUIDMixin, db


class AccountType(StrChoices):
    USER = "USER"
    SERVICE = "SERVICE"


class Account(UUIDMixin, CreatedAtMixin, db.Model):
    # Account can access the platform
    active = db.Column(db.BOOLEAN, nullable=False, server_default=db.text("TRUE"))
    # Administrator
    superuser = db.Column(db.BOOLEAN, nullable=False, server_default=db.text("FALSE"))

    # User account vs. service account
    type = db.Column(db.Enum(AccountType), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
    }


class UserAccount(Account):
    id = db.Column(
        Account.id.type, db.ForeignKey(Account.id, ondelete="CASCADE"), primary_key=True
    )
    # Email used to log in. Should always be lowercased
    email = db.Column(db.TEXT, nullable=False, unique=True)
    # Hashed password
    password = db.Column(db.TEXT, nullable=False)
    # First name
    first_name = db.Column(db.TEXT, nullable=False)
    # Last name
    last_name = db.Column(db.TEXT, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": AccountType.USER,
    }


class ServiceAccount(Account):
    id = db.Column(
        Account.id.type, db.ForeignKey(Account.id, ondelete="CASCADE"), primary_key=True
    )
    name = db.Column(db.TEXT, nullable=False, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": AccountType.SERVICE,
    }
