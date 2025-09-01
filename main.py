import asyncio
from aiogram import Bot, Dispatcher
from config.bot_config import BOT_TOKEN
from utils.logger import get_logger

from handlers.commands.base_commands import base_commands_router
from handlers.custom_handlers.feedback_help_handler import feedback_router
from handlers.custom_handlers.settings_handlers import settings_router
from handlers.custom_handlers.special_handlers import special_router
from handlers.custom_handlers.portfolio_handlers import portfolio_router
from handlers.custom_handlers.ideas_handlers import ideas_router
from handlers.custom_handlers.analysis_handlers import analysis_router

from db.init_db import init_db
from middleware.middleware import DbSessionMiddleware
from states.all_states import MemoryStorage




bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.update.outer_middleware(DbSessionMiddleware())

logger = get_logger(__name__)
dp.include_routers(base_commands_router,
                   feedback_router,
                   settings_router,
                   portfolio_router,
                   ideas_router,
                   analysis_router,
                   special_router,
)

async def main():
    logger.info('Bot starts working')
    try:
        await init_db()
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"Bot crashed: {e}", exc_info=True)

    finally:
        await bot.session.close()
        logger.info('Bot stopped')


if __name__ == "__main__":
    asyncio.run(main())