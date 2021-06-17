"""initial migration

Revision ID: f918bfd263ea
Revises: 
Create Date: 2021-06-14 22:13:21.027804

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f918bfd263ea"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("gender", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("cell", sa.String(length=32), nullable=True),
        sa.Column("nat", sa.String(length=8), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("street_number", sa.Integer(), nullable=True),
        sa.Column("street_name", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("postcode", sa.Integer(), nullable=True),
        sa.Column("latitude", sa.String(), nullable=True),
        sa.Column("longitude", sa.String(), nullable=True),
        sa.Column("timezone_offset", sa.String(), nullable=True),
        sa.Column("timezone_description", sa.String(), nullable=True),
        sa.Column("uuid", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("salt", sa.String(), nullable=True),
        sa.Column("md5", sa.String(length=32), nullable=True),
        sa.Column("sha1", sa.String(length=40), nullable=True),
        sa.Column("sha256", sa.String(length=64), nullable=True),
        sa.Column("date_of_birth", sa.String(length=32), nullable=True),
        sa.Column("age", sa.SmallInteger(), nullable=True),
        sa.Column("registered_date", sa.String(length=32), nullable=True),
        sa.Column("registered_age", sa.SmallInteger(), nullable=True),
        sa.Column("id_name", sa.String(), nullable=True),
        sa.Column("id_value", sa.String(), nullable=True),
        sa.Column("portrait_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("user_id"),

    )
    op.create_index(op.f("ix_users_user_id"), "users", ["user_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_users_user_id"), table_name="users")
    op.drop_table("users")
