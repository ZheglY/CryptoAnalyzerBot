from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession


from utils.logger import get_logger
from typing import Union

from keyboard.inline.inline_buttons import portfolio_button, menu_button, settings_button, help_keyboard

from services.portfolio_service import show_portfolio

from db.crud import get_or_create_user


logger = get_logger(__name__)
base_commands_router = Router()



@base_commands_router.message(CommandStart())
async def start_command(message: Message, session: AsyncSession, state:FSMContext):
    welcome_text = ("📊 Инвестиционный помощник  \n\n "
                    "💰 Мой портфель – баланс и доходность  \n"
                    "📈 Аналитика – рыночные индикаторы \n"
                    "🔍 Идеи – перспективные активы \n\n"
                    "⚙️ Настройки | ℹ️ Помощь  ")

    await state.clear()
    await get_or_create_user(session=session, tg_id=message.from_user.id)
    await message.answer(welcome_text, reply_markup=menu_button())


@base_commands_router.callback_query(F.data == 'go_menu')
@base_commands_router.message(Command('menu'))
async def menu_command(update: Union[Message, CallbackQuery]):
    welcome_text = ("📊 Инвестиционный помощник  \n\n "
                    "💰 Мой портфель – баланс и доходность  \n"
                    "📈 Аналитика – рыночные индикаторы \n"
                    "🔍 Идеи – перспективные активы \n\n"
                    "⚙️ Настройки | ℹ️ Помощь  ")


    if isinstance(update, CallbackQuery):
        await update.message.answer(welcome_text, reply_markup=menu_button())
        await update.answer()
    else:
        await update.answer(welcome_text, reply_markup=menu_button())


@base_commands_router.callback_query(F.data == "portfolio_button")
@base_commands_router.message(Command('portfolio'))
async def show_profile_command(update: Union[Message, CallbackQuery]):
    result = await show_portfolio(tg_id=update.from_user.id)
    portfolio_text = ('Ваш портфель: \n\n'
                      f'Текущая стоимость: {result.get('total_price')} {result.get('currency')}'
                      '\nИзменение за 24ч: '   
                      '\nРаспределение по активам (круговая диаграмма)' # будет присылать фоткой в чат а снизу подпись 
                      '\nЦель ценовых уровней')

    # функция Текущая стоимость
    # функция Изменение за 24ч:
    # функция Распределение по активам
    # функция Цель ценовых уровней
    if isinstance(update, CallbackQuery):
        await update.message.answer(portfolio_text, reply_markup=portfolio_button())
        await update.answer()
    else:
        await update.answer(portfolio_text, reply_markup=portfolio_button())


@base_commands_router.callback_query(F.data == "help_button")
@base_commands_router.message(Command('help'))
async def help_handler(update: Union[Message, CallbackQuery]):
    help_text = ('🆘 Краткая справка функционала\n\n'
                 'Основные команды:  \n\n/start – перезапустить бот '
                 '\n/portfolio – ваш портфель '
                 '\n/analytics – рыночная аналитика '
                 '\n/settings – настройки '
                 '\n\nЕсли вы нашли ошибку или желаете оставить отзыв используйте кнопку "Отзыв" ниже.')

    if isinstance(update, CallbackQuery):
        await update.message.answer(help_text, reply_markup=help_keyboard())
        await update.answer()
    else:
        await update.answer(help_text, reply_markup=help_keyboard())



@base_commands_router.callback_query(F.data == "settings_button")
@base_commands_router.message(Command('settings'))
async def settings_handler(update: Union[Message, CallbackQuery]):
    setting_text = (
        "В настройках вы можете изменить тип валюты, включить уведомления и привязать почту для получения отчетов по курсу интересующих вас валют \n\n"
        "Уведомления: Выкл"
                    "\nВалюта: USD"
                    "\nПочта: \n\n")

    if isinstance(update, CallbackQuery):
        await update.message.answer(setting_text, reply_markup=settings_button())
        await update.answer()
    else:
        await update.answer(setting_text, reply_markup=settings_button())






