"""add explicit varchar length limits

Revision ID: 9e1adc2c9b82
Revises: ade3b59f56d4
Create Date: 2026-07-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9e1adc2c9b82'
down_revision: Union[str, Sequence[str], None] = 'ade3b59f56d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'email', type_=sa.String(254), existing_type=sa.VARCHAR())
    op.alter_column('users', 'stack', type_=sa.String(500), existing_type=sa.VARCHAR())
    op.alter_column('users', 'city', type_=sa.String(100), existing_type=sa.VARCHAR())
    op.alter_column('users', 'work_type', type_=sa.String(50), existing_type=sa.VARCHAR())
    op.alter_column('users', 'bio', type_=sa.String(2000), existing_type=sa.VARCHAR())
    op.alter_column('users', 'resume_text', type_=sa.String(10000), existing_type=sa.VARCHAR())

    op.alter_column('vacancies', 'title', type_=sa.String(300), existing_type=sa.VARCHAR(), existing_nullable=False)
    op.alter_column('vacancies', 'company', type_=sa.String(300), existing_type=sa.VARCHAR())
    op.alter_column('vacancies', 'city', type_=sa.String(100), existing_type=sa.VARCHAR())
    op.alter_column('vacancies', 'salary', type_=sa.String(100), existing_type=sa.VARCHAR())
    op.alter_column('vacancies', 'work_type', type_=sa.String(50), existing_type=sa.VARCHAR())
    op.alter_column('vacancies', 'experience', type_=sa.String(100), existing_type=sa.VARCHAR())
    op.alter_column('vacancies', 'url', type_=sa.String(1000), existing_type=sa.VARCHAR(), existing_nullable=False)
    op.alter_column('vacancies', 'source', type_=sa.String(50), existing_type=sa.VARCHAR(), existing_nullable=False)

    op.alter_column('applications', 'note', type_=sa.String(1000), existing_type=sa.VARCHAR())


def downgrade() -> None:
    op.alter_column('applications', 'note', type_=sa.VARCHAR(), existing_type=sa.String(1000))

    op.alter_column('vacancies', 'source', type_=sa.VARCHAR(), existing_type=sa.String(50), existing_nullable=False)
    op.alter_column('vacancies', 'url', type_=sa.VARCHAR(), existing_type=sa.String(1000), existing_nullable=False)
    op.alter_column('vacancies', 'experience', type_=sa.VARCHAR(), existing_type=sa.String(100))
    op.alter_column('vacancies', 'work_type', type_=sa.VARCHAR(), existing_type=sa.String(50))
    op.alter_column('vacancies', 'salary', type_=sa.VARCHAR(), existing_type=sa.String(100))
    op.alter_column('vacancies', 'city', type_=sa.VARCHAR(), existing_type=sa.String(100))
    op.alter_column('vacancies', 'company', type_=sa.VARCHAR(), existing_type=sa.String(300))
    op.alter_column('vacancies', 'title', type_=sa.VARCHAR(), existing_type=sa.String(300), existing_nullable=False)

    op.alter_column('users', 'resume_text', type_=sa.VARCHAR(), existing_type=sa.String(10000))
    op.alter_column('users', 'bio', type_=sa.VARCHAR(), existing_type=sa.String(2000))
    op.alter_column('users', 'work_type', type_=sa.VARCHAR(), existing_type=sa.String(50))
    op.alter_column('users', 'city', type_=sa.VARCHAR(), existing_type=sa.String(100))
    op.alter_column('users', 'stack', type_=sa.VARCHAR(), existing_type=sa.String(500))
    op.alter_column('users', 'email', type_=sa.VARCHAR(), existing_type=sa.String(254))
