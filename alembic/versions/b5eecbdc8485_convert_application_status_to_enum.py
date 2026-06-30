"""Convert application status to enum

Revision ID: b5eecbdc8485
Revises: bd3ba32c7580
Create Date: 2026-06-30 08:21:36.855754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5eecbdc8485'
down_revision: Union[str, Sequence[str], None] = 'bd3ba32c7580'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    application_status_enum = sa.Enum(
        'applied', 'interview', 'offer', 'rejected', 'withdrawn',
        name='application_status'
    )
    application_status_enum.create(op.get_bind())
    op.alter_column(
        'applications', 'status',
        existing_type=sa.VARCHAR(),
        type_=application_status_enum,
        existing_nullable=False,
        postgresql_using='status::application_status'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'applications', 'status',
        existing_type=sa.Enum('applied', 'interview', 'offer', 'rejected', 'withdrawn', name='application_status'),
        type_=sa.VARCHAR(),
        existing_nullable=False
    )
    sa.Enum(name='application_status').drop(op.get_bind())
