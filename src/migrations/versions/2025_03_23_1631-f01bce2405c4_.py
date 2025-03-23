from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f01bce2405c4"
down_revision: Union[str, None] = "3e9d184cfa73"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "accounts",
        sa.Column("balance", sa.Float(), nullable=False),
        sa.Column("user_oid", sa.Integer(), nullable=False),
        sa.Column("oid", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_oid"], ["users.oid"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("oid"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("accounts")
