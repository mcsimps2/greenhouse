"""Add account schemas

Revision ID: ba9a95b323f1
Revises: 
Create Date: 2022-08-21 03:55:53.129570

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ba9a95b323f1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "active", sa.BOOLEAN(), server_default=sa.text("TRUE"), nullable=False
        ),
        sa.Column(
            "superuser", sa.BOOLEAN(), server_default=sa.text("FALSE"), nullable=False
        ),
        sa.Column(
            "type", sa.Enum("USER", "SERVICE", name="accounttype"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_account")),
    )
    op.create_table(
        "service_account",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["account.id"],
            name=op.f("fk_service_account_id_account"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_service_account")),
        sa.UniqueConstraint("name", name=op.f("uq_service_account_name")),
    )
    op.create_table(
        "user_account",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("email", sa.TEXT(), nullable=False),
        sa.Column("password", sa.TEXT(), nullable=False),
        sa.Column("first_name", sa.TEXT(), nullable=False),
        sa.Column("last_name", sa.TEXT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["account.id"],
            name=op.f("fk_user_account_id_account"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_account")),
        sa.UniqueConstraint("email", name=op.f("uq_user_account_email")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_account")
    op.drop_table("service_account")
    op.drop_table("account")
    # ### end Alembic commands ###