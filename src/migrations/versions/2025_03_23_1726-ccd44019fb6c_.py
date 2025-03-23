from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "ccd44019fb6c"
down_revision: Union[str, None] = "f01bce2405c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "transactions",
        sa.Column("oid", sa.String(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("account_oid", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("amount > 0", name="pos_amount_constr"),
        sa.ForeignKeyConstraint(["account_oid"], ["accounts.oid"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("oid"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("transactions")
