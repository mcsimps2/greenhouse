from app.util.choices import StrChoices
from .account import Account
from .greenhouse import Greenhouse
from .orm import UUIDMixin, db


class Role(StrChoices):
    # Can insert data on behalf of a greenhouse
    SAMPLER = "SAMPLER"
    # Can configure a greenhouse
    MANAGER = "MANAGER"


class AccountGreenhouseRole(UUIDMixin, db.Model):
    """Dictates which accounts can control a greenhouse"""

    account_id = db.Column(
        Account.id.type, db.ForeignKey(Account.id, ondelete="CASCADE"), nullable=False
    )
    greenhouse_id = db.Column(
        Greenhouse.id.type,
        db.ForeignKey(Greenhouse.id, ondelete="CASCADE"),
        nullable=False,
    )
    role = db.Column(db.Enum(Role), nullable=False)

    account = db.relationship(
        Account,
        backref=db.backref(
            "greenhouses", cascade="all, delete, delete-orphan", passive_deletes=True
        ),
    )
    greenhouse = db.relationship(
        Greenhouse,
        backref=db.backref(
            "accounts", cascade="all, delete, delete-orphan", passive_deletes=True
        ),
    )

    __table_args__ = (db.UniqueConstraint("account_id", "greenhouse_id", "role"),)
