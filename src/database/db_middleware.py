from aiogram import BaseMiddleware
from aiogram.types import Update
from database.db import get_async_session


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        async_session = await get_async_session()
        async with async_session as session:
            data["db"] = session
            return await handler(event, data)