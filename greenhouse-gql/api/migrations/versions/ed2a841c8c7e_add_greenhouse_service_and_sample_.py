"""Add greenhouse, service, and sample schemas

Revision ID: ed2a841c8c7e
Revises: ba9a95b323f1
Create Date: 2022-08-28 21:08:41.873499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ed2a841c8c7e"
down_revision = "ba9a95b323f1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "greenhouse",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_greenhouse")),
        sa.UniqueConstraint("name", name=op.f("uq_greenhouse_name")),
    )
    op.create_table(
        "account_greenhouse_role",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("account_id", postgresql.UUID(), nullable=False),
        sa.Column("greenhouse_id", postgresql.UUID(), nullable=False),
        sa.Column("role", sa.Enum("SAMPLER", "MANAGER", name="role"), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
            name=op.f("fk_account_greenhouse_role_account_id_account"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["greenhouse_id"],
            ["greenhouse.id"],
            name=op.f("fk_account_greenhouse_role_greenhouse_id_greenhouse"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_account_greenhouse_role")),
        sa.UniqueConstraint(
            "account_id",
            "greenhouse_id",
            "role",
            name=op.f("uq_account_greenhouse_role_account_id_greenhouse_id_role"),
        ),
    )
    op.create_table(
        "service",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("greenhouse_id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("ON", "OFF", "AUTO", name="servicestatus"),
            server_default=sa.text("'AUTO'"),
            nullable=False,
        ),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(
            ["greenhouse_id"],
            ["greenhouse.id"],
            name=op.f("fk_service_greenhouse_id_greenhouse"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_service")),
        sa.UniqueConstraint(
            "greenhouse_id", "name", name=op.f("uq_service_greenhouse_id_name")
        ),
    )
    op.create_table(
        "sample",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("greenhouse_id", postgresql.UUID(), nullable=False),
        sa.Column("service_id", postgresql.UUID(), nullable=False),
        sa.Column("measurement", sa.DECIMAL(), nullable=False),
        sa.ForeignKeyConstraint(
            ["greenhouse_id"],
            ["greenhouse.id"],
            name=op.f("fk_sample_greenhouse_id_greenhouse"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["service.id"],
            name=op.f("fk_sample_service_id_service"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sample")),
    )
    op.create_index(
        "ix_sample_created_at",
        "sample",
        [sa.text("created_at DESC")],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("service")
    op.drop_index("ix_sample_created_at", table_name="sample")
    op.drop_table("sample")
    op.drop_table("account_greenhouse_role")
    op.drop_table("greenhouse")
    # ### end Alembic commands ###
