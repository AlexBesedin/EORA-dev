import logging
from aiogram import F, types, Router, Dispatcher
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from contants.constants import (
    PROCESSING_MESSAGE, 
    RATING_PROMPT_TEXT, 
    THANK_YOU_TEXT, 
    WELCOME_MESSAGE
)
from keyboards.keyboards import get_rating_keyboard
from services import response_generator
from services.project_service import get_projects_by_similar_tags
from services.rating_service import save_rating


logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message, db: AsyncSession):
    await message.answer(WELCOME_MESSAGE)
    return


@router.message(F.text)
async def handle_user_query(message: types.Message, db: AsyncSession):
    user_query = message.text
    processing_message = await message.answer(PROCESSING_MESSAGE)
    try:
        matching_projects, response_time = await get_projects_by_similar_tags(db, user_query)
        response = response_generator.generate_response(user_query, matching_projects)
        await message.answer(response, parse_mode="HTML")
        
        if matching_projects:
            first_project = matching_projects[0]
            project_id = first_project['id']
            similarity = first_project['similarity_score']
            await message.answer(
                RATING_PROMPT_TEXT, 
                parse_mode="HTML", 
                reply_markup=get_rating_keyboard(project_id, similarity, response_time)
            )
    finally:
        await processing_message.delete()


@router.callback_query(lambda c: c.data and c.data.startswith('rate_'))
async def process_rating(callback_query: types.CallbackQuery, db: AsyncSession):
    """
    Обработчик для получения оценки от пользователя с привязкой к проекту.
    """
    user_id = callback_query.from_user.id

    data = callback_query.data.split('_')
    rating = int(data[1])
    project_id = int(data[2])
    similarity = float(data[3])
    response_time = float(data[4])

    await save_rating(db, user_id, project_id, rating, similarity, response_time)
    await callback_query.message.answer(THANK_YOU_TEXT.format(rating=rating))
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()










def register_handlers_start(dp: Dispatcher):
    dp.include_router(router)