"""Load projects data

Revision ID: f7a79b5180d6
Revises: a1b2c3d4e5f6
Create Date: 2024-09-05 19:58:50.210917

"""

from typing import Sequence, Union

import os
from alembic import op
import json
import sqlalchemy as sa

from config import BASE_DIR


# revision identifiers, used by Alembic.
revision: str = "f7a79b5180d6"
down_revision: Union[str, None] = "8af2d735d922"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Путь к файлу с данными
DIR_JSON = BASE_DIR / "data" / "data_with_tags.json"


def upgrade() -> None:
    # Загрузка данных из JSON файла
    if not os.path.exists(DIR_JSON):
        print(f"Warning: Файл {DIR_JSON} не найден. Данные не были загружены.")
        return

    with open(DIR_JSON, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    print(projects)

    projects_table = sa.Table(
        'projects',
        sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('url', sa.String(length=2083), nullable=False),
        sa.Column('company', sa.String(length=255), nullable=True),
        sa.Column('problem', sa.Text, nullable=True),
        sa.Column('solution', sa.Text, nullable=True),
        sa.Column('tags', sa.ARRAY(sa.String), nullable=True)
    )

    # Вставка данных в таблицу projects, включая поле tags
    op.bulk_insert(
        projects_table,
        [
            {
                "title": project["title"],
                "url": project["url"],
                "company": project["company"],
                "problem": project["problem"],
                "solution": project["solution"],
                "tags": project.get("tags", [])
            }
            for project in projects
        ]
    )

def downgrade() -> None:
    # Удаление всех записей из таблицы projects
    op.execute("DELETE FROM projects")