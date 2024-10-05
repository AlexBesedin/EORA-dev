import asyncio
import logging

from loader import init_bot

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



async def main():
    bot, dp = await init_bot()

    try:
        logger.info("Removing webhook...")
        await bot.delete_webhook()
        
        logger.info("Starting bot polling...")
        await dp.start_polling(bot)
    finally:
        logger.info("Closing bot session...")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"An error occurred while running the bot: {e}")