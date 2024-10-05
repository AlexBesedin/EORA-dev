import logging

from aiogram import F, types, Router, Dispatcher
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from contants.constants import PROCESSING_MESSAGE, WELCOME_MESSAGE
from services import response_generator
from services.project_service import get_projects_by_similar_tags

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
        matching_projects = await get_projects_by_similar_tags(db, user_query)
        response = response_generator.generate_response(user_query, matching_projects)
        await message.answer(response, parse_mode="HTML")
    finally:
        await processing_message.delete()


def register_handlers_start(dp: Dispatcher):
    dp.include_router(router)