import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from bot.config import load_settings
from bot.handlers import ask_question, menu, start
from bot.services.content import ContentRepository


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    settings = load_settings()
    content = ContentRepository(settings.data_dir)

    session = AiohttpSession(proxy=settings.telegram_proxy_url)
    bot = Bot(token=settings.bot_token, session=session)

    dispatcher = Dispatcher(settings=settings, content=content)
    dispatcher.include_router(start.router)
    dispatcher.include_router(ask_question.router)
    dispatcher.include_router(menu.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
