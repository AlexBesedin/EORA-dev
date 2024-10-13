from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, List
from models.projects import Project


class CRUDProject:
    def __init__(self, model):
        self.model = model

    async def get_all_projects(self, db: AsyncSession) -> List[dict]:
        result = await db.execute(select(self.model))
        return result.scalars().all()
    

    async def get_all_projects_with_embeddings(self, db: AsyncSession) -> List[Dict]:
        result = await db.execute(
            select(
                self.model.id,
                self.model.title,
                self.model.url,
                self.model.company,
                self.model.tags,
                self.model.embedding,
                self.model.problem,
                self.model.solution
            )
        )
        return result.mappings().all()

crud_project = CRUDProject(Project)
