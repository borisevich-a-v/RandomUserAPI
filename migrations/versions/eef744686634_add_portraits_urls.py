"""add portraits urls

Revision ID: eef744686634
Revises: e5e5e3cb1073
Create Date: 2021-06-16 13:42:48.175677

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "eef744686634"
down_revision = "e5e5e3cb1073"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("portrait_large", sa.String(), nullable=True))
    op.add_column("users", sa.Column("portrait_thumbnail", sa.String(), nullable=True))


def downgrade():
    op.drop_column("users", "portrait_thumbnail")
    op.drop_column("users", "portrait_large")
