from aiogram import BaseMiddleware
from db.models import async_session
from utils.logger import get_logger


logger = get_logger(__name__)


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with async_session() as session:
            data["session"] = session
            try:
                logger.debug(f"Before handler | State: {await data['state'].get_state()}")
                result = await handler(event, data)
                await session.commit()
                logger.debug(f"After handler | State: {await data['state'].get_state()}")
                return result
            except Exception as e:
                logger.error(f"Middleware error: {e}")
                await session.rollback()
                raise
            finally:
                if session.in_transaction():
                    await session.rollback()
                await session.close()
                logger.debug("Session closed")
