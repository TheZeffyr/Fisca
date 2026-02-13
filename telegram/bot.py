import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers import routers
from config import Config
from logger.setup import setup_logging
from middlewares import RegistrationMiddleware



logger = logging.getLogger(__name__)


async def start():
    setup_logging()
    logger.info("Fisca bot starting...")
    bot = Bot(
        Config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN_V2
            )
        )

    dp = Dispatcher()
    dp.include_routers(*routers)
    dp.message.middleware(RegistrationMiddleware())
    dp.callback_query.middleware(RegistrationMiddleware())
    logger.info("Bot initialized, starting polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())