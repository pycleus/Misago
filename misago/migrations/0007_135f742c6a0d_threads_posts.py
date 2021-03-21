"""threads_posts

Revision ID: 135f742c6a0d
Revises: f386c9e48425
Create Date: 2019-12-16 17:32:58.038680

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "135f742c6a0d"
down_revision = "f386c9e48425"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "misago_threads",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("first_post_id", sa.Integer(), nullable=True),
        sa.Column("starter_id", sa.Integer(), nullable=True),
        sa.Column("starter_name", sa.String(length=255), nullable=False),
        sa.Column("last_post_id", sa.Integer(), nullable=True),
        sa.Column("last_poster_id", sa.Integer(), nullable=True),
        sa.Column("last_poster_name", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_posted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("replies", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_closed", sa.Boolean(), nullable=False),
        sa.Column("extra", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["misago_categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["last_poster_id"], ["misago_users.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["starter_id"], ["misago_users.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "misago_threads_order",
        "misago_threads",
        [sa.text("last_post_id DESC"), "category_id"],
        unique=False,
    )
    op.create_table(
        "misago_posts",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("thread_id", sa.Integer(), nullable=False),
        sa.Column("poster_id", sa.Integer(), nullable=True),
        sa.Column("poster_name", sa.String(length=255), nullable=False),
        sa.Column("markup", sa.Text(), nullable=False),
        sa.Column("rich_text", sa.JSON(), nullable=False),
        sa.Column("edits", sa.Integer(), nullable=False),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("extra", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["misago_categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["poster_id"], ["misago_users.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["thread_id"], ["misago_threads.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key(
        None,
        "misago_threads",
        "misago_posts",
        ["first_post_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        None,
        "misago_threads",
        "misago_posts",
        ["last_post_id"],
        ["id"],
        ondelete="SET NULL",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "misago_threads", type_="foreignkey")
    op.drop_table("misago_posts")
    op.drop_index("misago_threads_order", table_name="misago_threads")
    op.drop_table("misago_threads")
    # ### end Alembic commands ###
