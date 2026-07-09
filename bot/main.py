import asyncio
import logging
import sys

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.config import load_settings
from bot.config import Settings
from bot.handlers import ask_question, menu, start
from bot.services.content import ContentRepository


def create_dispatcher(settings: Settings) -> Dispatcher:
    content = ContentRepository(settings.data_dir)
    dispatcher = Dispatcher(settings=settings, content=content)
    dispatcher.include_router(start.router)
    dispatcher.include_router(ask_question.router)
    dispatcher.include_router(menu.router)
    return dispatcher


def create_bot(settings: Settings) -> Bot:
    session = AiohttpSession(proxy=settings.telegram_proxy_url)
    return Bot(token=settings.bot_token, session=session)


async def run_polling(settings: Settings) -> None:
    bot = create_bot(settings)
    dispatcher = create_dispatcher(settings)
    await bot.delete_webhook(drop_pending_updates=False)
    await dispatcher.start_polling(bot)


async def on_webhook_startup(bot: Bot, settings: Settings) -> None:
    if not settings.webhook_base_url:
        raise RuntimeError(
            "Для BOT_MODE=webhook нужно задать WEBHOOK_BASE_URL "
            "или WEBHOOK_HOSTNAME."
        )

    webhook_url = f"{settings.webhook_base_url.rstrip('/')}{settings.webhook_path}"
    await bot.set_webhook(webhook_url, secret_token=settings.webhook_secret)
    logging.info("Webhook установлен: %s", webhook_url)


def run_webhook(settings: Settings) -> None:
    bot = create_bot(settings)
    dispatcher = create_dispatcher(settings)
    dispatcher.startup.register(on_webhook_startup)

    app = web.Application()

    async def healthcheck(_: web.Request) -> web.Response:
        return web.Response(text="MPT admission bot is running")

    app.router.add_get("/", healthcheck)

    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=settings.webhook_secret,
    ).register(app, path=settings.webhook_path)

    setup_application(app, dispatcher, bot=bot, settings=settings)
    web.run_app(app, host=settings.web_host, port=settings.web_port)


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    settings = load_settings()
    if settings.bot_mode == "webhook":
        run_webhook(settings)
        return

    if settings.bot_mode != "polling":
        raise RuntimeError("BOT_MODE должен быть polling или webhook.")

    asyncio.run(run_polling(settings))


if __name__ == "__main__":
    main()
