"""Add current account function

Revision ID: 4f505611bde7
Revises: ed2a841c8c7e
Create Date: 2022-09-05 19:38:34.767815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f505611bde7'
down_revision = 'ed2a841c8c7e'
branch_labels = None
depends_on = None


def upgrade():
    sa.schema.DDL("""
    CREATE FUNCTION current_account(hasura_session JSON) RETURNS account AS $$
        SELECT * FROM account WHERE id = UUID(hasura_session ->> 'x-hasura-account-id');
    $$ LANGUAGE sql STABLE;
    """)(target=None, bind=op.get_bind())


def downgrade():
    sa.schema.DDL("DROP FUNCTION current_account;")
