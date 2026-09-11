"""add attendance unique constraint

Revision ID: 94ba403f72db
Revises: 847814d488bb
Create Date: 2026-09-10 10:50:49.653487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94ba403f72db'
down_revision: Union[str, Sequence[str], None] = '847814d488bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_attendance_session_student",
        "attendance_records",
        ["sessionID", "studentID"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_attendance_session_student",
        "attendance_records",
        type_="unique",
    )
