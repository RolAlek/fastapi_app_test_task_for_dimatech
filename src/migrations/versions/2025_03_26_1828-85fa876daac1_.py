from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "85fa876daac1"
down_revision: Union[str, None] = "e941ff69b3a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.drop_column("accounts", "balance")
    op.create_index(op.f("ix_transactions_oid"), "transactions", ["oid"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f("ix_transactions_oid"), table_name="transactions")
    op.add_column(
        "accounts",
        sa.Column(
            "balance",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
    )
