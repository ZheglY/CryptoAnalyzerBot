from db.models import Base, engine
from utils.logger import get_logger


logger = get_logger(__name__)

async def init_db():
    """
    Создает таблицы в базе данных.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.debug('Создание бд')