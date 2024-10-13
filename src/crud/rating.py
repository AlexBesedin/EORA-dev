from sqlalchemy.ext.asyncio import AsyncSession
from models.rating import Rating


class CRUDProject:
    def __init__(self, model):
        self.model = model

    async def create(self, db: AsyncSession, obj_in: Rating) -> Rating:
        db.add(obj_in)
        await db.commit()
        await db.refresh(obj_in)
        return obj_in


crud_rating = CRUDProject(Rating)