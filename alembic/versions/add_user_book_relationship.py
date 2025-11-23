"""Add user-book relationship

Revision ID: 1235
Revises: 1234
Create Date: 2025-11-18 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1235'
down_revision = '1234'
branch_labels = None
depends_on = None


def upgrade():
    # This is a no-op because we're just adding a relationship, not changing the schema
    # The relationship is defined in the models but doesn't require database changes
    pass


def downgrade():
    # No need to do anything for downgrade as we didn't change the schema
    pass
