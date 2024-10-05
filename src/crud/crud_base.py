from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from models.projects import Project


class CRUDProject:
    def __init__(self, model):
        self.model = model

    async def get_all_projects(self, db: AsyncSession) -> List[dict]:
        result = await db.execute(select(self.model))
        return result.scalars().all()


crud_project = CRUDProject(Project)
