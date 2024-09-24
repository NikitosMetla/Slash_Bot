import asyncio

from aiogram import Dispatcher, Bot

from db.engine import DatabaseEngine
from handlers.chat_gpt_handlers import chat_gpt_router
from handlers.design_level_handler import design_level_router
from handlers.earnings_level_handler import earnings_level_router
from handlers.mentor_handler import mentor_router
from handlers.send_link_handler import send_link_router
from settings import storage_bot, token_design_level

design_bot = Bot(token=token_design_level, parse_mode="html")


async def main():
    # db_engine = DatabaseEngine()
    # await db_engine.proceed_schemas()
    print(await design_bot.get_me())
    await design_bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher(storage=storage_bot)
    dp.include_routers(mentor_router, design_level_router, earnings_level_router, send_link_router, chat_gpt_router)
    await dp.start_polling(design_bot)


if __name__ == "__main__":
    asyncio.run(main())
