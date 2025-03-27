"""Test users create

Revision ID: 94397c6312de
Revises: 85fa876daac1
Create Date: 2025-03-27 12:16:01.622353

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from src.core.settings import AuthSettings, get_settings
from src.repositories.token import _TokenRepository
from src.repositories.user import _UserRepository
from src.services.modules.authentication.service import _AuthenticationService

# revision identifiers, used by Alembic.
revision: str = "94397c6312de"
down_revision: Union[str, None] = "85fa876daac1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    settings: AuthSettings = get_settings(AuthSettings)
    service = _AuthenticationService(
        settings=settings,
        token_repository=_TokenRepository,
        user_repository=_UserRepository,
    )
    user_hashed_password = service.get_pwd_hash("usersecretstring")
    admin_hashed_password = service.get_pwd_hash("adminsecretstring")

    op.execute(
        sa.text(
            f"""
            INSERT INTO users (oid, email, hashed_password, first_name, last_name, is_admin) VALUES
               (1, 'user@example.com', '{user_hashed_password}', 'Ringo', 'Starr', FALSE);
            """
        )
    )

    op.execute(
        sa.text(
            """
            INSERT INTO accounts (oid, user_oid) VALUES (1, 1);
            """
        )
    )

    op.execute(
        sa.text(
            f"""
            INSERT INTO users (oid, email, hashed_password, first_name, last_name, is_admin) VALUES
                (2, 'admin@example.com', '{admin_hashed_password}', 'John', 'Doe', TRUE);
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            """
            DELETE FROM users WHERE oid IN (1, 2);
            """
        )
    )
    op.execute(
        sa.text(
            """
            DELETE FROM accounts WHERE oid = 1;
            """
        )
    )
