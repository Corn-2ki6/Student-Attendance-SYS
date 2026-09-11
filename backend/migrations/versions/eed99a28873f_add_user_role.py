"""add user role

Revision ID: eed99a28873f
Revises: 94ba403f72db
Create Date: 2026-09-10
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eed99a28873f"
down_revision: Union[str, Sequence[str], None] = "94ba403f72db"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
            server_default="STUDENT",
        ),
    )

    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "role")