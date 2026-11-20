"""add unique index on lower skill name

Revision ID: c23dde856537
Revises: c0725d329bb7
Create Date: 2026-11-20 15:12:06.845036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c23dde856537'
down_revision: Union[str, Sequence[str], None] = 'c0725d329bb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        "uq_skills_name_lower",
        "skills",
        [sa.text("lower(name)")],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("uq_skills_name_lower", table_name="skills")
