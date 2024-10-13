"""add rating

Revision ID: c6bf9062ee8c
Revises: d38341733b04
Create Date: 2024-10-13 10:03:48.587986

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c6bf9062ee8c'
down_revision: Union[str, None] = 'd38341733b04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создаем таблицу для хранения оценок с привязкой к проектам
    op.create_table(
        'ratings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('similarity', sa.Float, nullable=False),
        sa.Column('response_time', sa.Float, nullable=False)
    )

def downgrade():
    # Удаляем таблицу
    op.drop_table('ratings')


