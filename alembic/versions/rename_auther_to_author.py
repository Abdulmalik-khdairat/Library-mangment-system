"""rename auther to author

Revision ID: 1234
Revises: d7cb50209e81
Create Date: 2025-11-18 09:55:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1234'
down_revision = 'd7cb50209e81'
branch_labels = None
depends_on = None


def upgrade():
    # Rename the column
    op.alter_column('books', 'auther_id', new_column_name='author_id')
    # If you have a foreign key constraint, you might need to drop and recreate it
    op.drop_constraint('books_auther_id_fkey', 'books', type_='foreignkey')
    op.create_foreign_key('books_author_id_fkey', 'books', 'users', ['author_id'], ['id'])


def downgrade():
    # Reverse the changes for rollback
    op.drop_constraint('books_author_id_fkey', 'books', type_='foreignkey')
    op.alter_column('books', 'author_id', new_column_name='auther_id')
    op.create_foreign_key('books_auther_id_fkey', 'books', 'users', ['auther_id'], ['id'])
