from sqlalchemy.ext.asyncio import AsyncSession

from models.rating import Rating
from crud.rating import crud_rating


async def save_rating(
    db: AsyncSession, 
    user_id: int, 
    project_id: int, 
    rating: int, 
    similarity: float,
    response_time: float,
):
    new_rating = Rating(
        user_id=user_id,
        project_id=project_id,
        rating=rating,
        similarity=similarity,
        response_time=response_time
    )
    await crud_rating.create(db, new_rating)