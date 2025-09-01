from sqlalchemy import update, select, insert
from db.models import User, Portfolio

from sqlalchemy.ext.asyncio import AsyncSession

from utils.logger import get_logger



logger = get_logger(__name__)


async def get_or_create_user(session: AsyncSession, tg_id: int):
    """
    Получает пользователя по Telegram ID или создает нового.
    """

    stmt = select(User).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        logger.info("Создание нового пользователя в get_or_create_user()")
        user = User(tg_id=tg_id, feedback="")
        session.add(user)
        await session.commit()
    else:
        logger.info("Пользователь уже существует | get_or_create_user()")



async def save_user_feedback(session: AsyncSession, tg_id: int, text: str):
    """
    Сохранение пользовательского отзыва в бд
    """
    try:
        request = (
            update(User)
            .where(User.tg_id == tg_id)
            .values(feedback=text)
        )
        await session.execute(request)
        await session.commit()

    except Exception as e:
        await session.rollback()
        logger.error(f"Error saving feedback for {tg_id}: {e}")
        raise


async def change_or_get_currency(session: AsyncSession, tg_id: int, currency=None):
    """ Если пользователь не указывает параметр currency, то просто получает текущую валюту
    Иначе изменяет ее на указанную валюту"""
    if not currency:
        request = (
            select(User.currency)
            .where(User.tg_id == tg_id)
        )
        result = await session.execute(request)
        user_currency = result.scalar()
        return user_currency

    try:
        request = (
            update(User)
            .where(User.tg_id == tg_id)
            .values(currency=currency)
        )
        await session.execute(request)
        await session.commit()

    except Exception as e:
        await session.rollback()
        logger.error(f"Error saving feedback for {tg_id}: {e}")
        raise


async def save_user_coin(session: AsyncSession, tg_id: int, coin_id: str, amount: float):
    """
    Сохранение монеты в портфолио пользователя
    """
    try:
        new_coin = Portfolio(user_id=tg_id, coin_id=coin_id, amount=amount)
        session.add(new_coin)
        await session.commit()
        logger.info(f'Монета {coin_id} в количестве {amount} успешно сохранена!')

    except Exception as e:
        await session.rollback()
        logger.error(f"Error saving feedback for {tg_id}: {e}")
        raise


async def save_email(session: AsyncSession, tg_id: int, email: str):
    """
    Сохранение почты в бд
    """
    stmt = select(User).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise ValueError("User not found")

    user.email = email
    await session.commit()
    logger.info(f'Почта {email} сохранена для пользователя {tg_id}!')


async def get_user_balance(session: AsyncSession, tg_id: int):
    """
    Получает баланс пользователя
    """

    stmt = select(Portfolio.coin_id, Portfolio.amount).where(Portfolio.user_id == tg_id)
    result = await session.execute(stmt, {"user_id": tg_id})
    data = result.all()

    if data is None:
        logger.debug(f"Баланс не найден | {data}")
        return None
    else:
        logger.debug(f"Баланс пользователя {data}")
        return data