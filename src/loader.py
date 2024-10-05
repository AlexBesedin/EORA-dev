from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config

from database.db_middleware import DbSessionMiddleware
from handlers.message_handlers import register_handlers_start

async def init_bot():
    bot = Bot(token=Config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    register_handlers_start(dp)

    dp.update.middleware(DbSessionMiddleware())
    
    
    return bot, dp