import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from utils.logger import get_logger
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud import change_or_get_currency, save_email
from handlers.commands.base_commands import menu_command
from states.all_states import EmailInput


settings_router = Router()
logger = get_logger(__name__)


@settings_router.callback_query(lambda c: c.data.startswith('currency_'))
async def change_currency(callback: CallbackQuery, session: AsyncSession):
    new_currency = callback.data[-3:]
    logger.info(f'Изменение валюты на {new_currency}')
    await change_or_get_currency(tg_id=callback.from_user.id, session=session, currency=new_currency)
    await callback.message.answer('Валюта успешна изменена')
    await menu_command(callback)
    await callback.message.delete()


@settings_router.callback_query(F.data == 'email_button')
async def email_handler(callback: CallbackQuery, state:FSMContext):
    await callback.message.answer('Введите свой email')
    await callback.answer()
    await state.set_state(EmailInput.check_email)


@settings_router.message(EmailInput.check_email)
async def email_handler(message: Message, state:FSMContext, session: AsyncSession):
    users_email = message.text.strip().lower()
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', users_email):
        raise ValueError("Invalid email format")

    await save_email(session=session, tg_id=message.from_user.id, email=users_email)
    await message.answer('Ваш email успешно привязан!')
    await state.clear()