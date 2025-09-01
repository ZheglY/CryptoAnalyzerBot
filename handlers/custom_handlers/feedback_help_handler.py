from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from states.all_states import FeedbackState
from db.crud import save_user_feedback
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.commands.base_commands import menu_command
from utils.logger import get_logger


feedback_router = Router()
logger = get_logger(__name__)


@feedback_router.callback_query(F.data == 'feedback_button')
async def feedback_handler(callback: CallbackQuery, state:FSMContext):
    text = 'Напишите подробнее о найденой ошибке или о ваших предложениях по улучшению продукта'

    await callback.message.answer(text)
    await callback.answer()
    await state.set_state(FeedbackState.get_feedback)


@feedback_router.message(FeedbackState.get_feedback)
async def save_feedback(message: Message, state:FSMContext, session: AsyncSession):
    text = 'Спасибо за отзыв. Ваше мнение крайне важно для нас!'
    await save_user_feedback(session=session, tg_id=message.from_user.id, text=message.text)
    await message.answer(text)

    await state.clear()
    await menu_command(message)