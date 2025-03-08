"""rename Breast column

Revision ID: 48fd0412c2ae
Revises: 
Create Date: 2025-03-08 19:37:16.531665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48fd0412c2ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('BreastfeedingSessions', 'Breast', existing_type=sa.String(10), new_column_name='BreastSide')


def downgrade() -> None:
    pass
