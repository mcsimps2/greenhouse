from sqlalchemy.dialects.postgresql import JSONB

from app.util.choices import StrChoices
from .orm import db, UUIDMixin, CreatedAtMixin


class ServiceStatus(StrChoices):
    ON = "ON"
    OFF = "OFF"
    AUTO = "AUTO"


class Greenhouse(UUIDMixin, CreatedAtMixin, db.Model):
    # Unique name of greenhouse
    name = db.Column(db.TEXT, nullable=False, unique=True)


class Service(UUIDMixin, db.Model):
    greenhouse_id = db.Column(
        Greenhouse.id.type,
        db.ForeignKey(Greenhouse.id, ondelete="CASCADE"),
        nullable=False,
    )
    name = db.Column(db.TEXT, nullable=False)
    status = db.Column(
        db.Enum(ServiceStatus),
        nullable=False,
        server_default=db.text(f"'{ServiceStatus.AUTO}'"),
    )
    # Each service has its own unique configuration, so use JSONB type
    config = db.Column(JSONB, nullable=True)

    greenhouse = db.relationship(
        Greenhouse,
        backref=db.backref(
            "services", cascade="all, delete, delete-orphan", passive_deletes=True
        ),
    )

    __table_args__ = (db.UniqueConstraint("greenhouse_id", "name"),)


class Sample(UUIDMixin, CreatedAtMixin, db.Model):
    greenhouse_id = db.Column(
        Greenhouse.id.type,
        db.ForeignKey(Greenhouse.id, ondelete="CASCADE"),
        nullable=False,
    )
    service_id = db.Column(
        Service.id.type, db.ForeignKey(Service.id, ondelete="CASCADE"), nullable=False
    )
    measurement = db.Column(db.DECIMAL, nullable=False)

    greenhouse = db.relationship(
        Greenhouse,
        backref=db.backref(
            "samples", cascade="all, delete, delete-orphan", passive_deletes=True
        ),
    )
    service = db.relationship(
        Service,
        backref=db.backref(
            "samples", cascade="all, delete, delete-orphan", passive_deletes=True
        ),
    )

    __table_args__ = (
        db.Index(
            "ix_sample_created_at",
            db.text("created_at DESC"),
        ),
    )
