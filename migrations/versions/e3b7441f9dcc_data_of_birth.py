"""data_of_birth

Revision ID: e3b7441f9dcc
Revises: 07e8e0607ebb
Create Date: 2021-06-13 15:41:44.693992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3b7441f9dcc'
down_revision = '07e8e0607ebb'
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column('users', 'data_of_birth', new_column_name='date_of_birth')



def downgrade():
    op.alter_column('users', 'date_of_birth', new_column_name='date_of_birth')
    # ### end Alembic commands ###
