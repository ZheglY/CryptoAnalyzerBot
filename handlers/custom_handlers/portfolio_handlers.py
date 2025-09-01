from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from services.portfolio_service import show_top_coins_service
from states.all_states import SearchCoins
from keyboard.inline.inline_buttons import top_coins_buttons
from utils.logger import get_logger
from handlers.commands.base_commands import show_profile_command
from sqlalchemy.ext.asyncio import AsyncSession

from services.portfolio_service import add_coin_info
from db.crud import save_user_coin


portfolio_router = Router()
logger = get_logger(__name__)


@portfolio_router.callback_query(F.data == 'add_asset')
async def add_asset_handler(callback: CallbackQuery, state:FSMContext):
    coins_list = await show_top_coins_service(tg_id=callback.from_user.id, limit=10)
    text = ('Выберите новый актив из самых популярных на данный момент монет ниже, '
            'или найдите интересующий Вас, написав название в чате\n\n'
            'Всю информацию о монете можно узнать в разделе Анализ')
    await callback.message.answer(text, reply_markup=top_coins_buttons(coins_list))
    await state.set_state(SearchCoins.search_coins)
    await callback.answer()


@portfolio_router.callback_query(lambda c: c.data.startswith('AddCoin_'))
async def save_button_amount_handler(callback: CallbackQuery, state: FSMContext):
    coin_id = callback.data.split('_')[1]
    coin_name, coin_price, currency = await add_coin_info(coin_id=coin_id, tg_id=callback.from_user.id)

    await state.update_data(coin_id=coin_id)

    await callback.message.answer(f'Монета: {coin_name} \n'
                                  f'Стоимость монеты: {coin_price} {currency}\n\n'
                                  'Сколько покупаете? (можно указать в дробных числах)')

    await state.set_state(SearchCoins.coins_amount)
    await callback.answer()


@portfolio_router.message(SearchCoins.search_coins)
async def save_typed_amount_handler(message: Message, state: FSMContext):
    coin_id = message.data.split('_')[1]
    coin_name, coin_price, currency = await add_coin_info(coin_id=coin_id, tg_id=message.from_user.id)

    await state.update_data(coin_id=coin_id)

    await message.answer(f'Монета: {coin_name} \n'
                                  f'Стоимость монеты: {coin_price} {currency}\n\n'
                                  'Сколько покупаете? (можно указать в дробных числах)')

    await state.set_state(SearchCoins.coins_amount)



@portfolio_router.message(SearchCoins.coins_amount)
async def save_coin_handler(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer('Монеты успешна добавлена!')

    data = await state.get_data()
    coin_id = data.get('coin_id')
    amount = float(message.text)

    await save_user_coin(session=session, tg_id=message.from_user.id, coin_id=coin_id, amount=amount)
    await state.clear()
    await show_profile_command(message)


@portfolio_router.callback_query(F.data == 'show_analytics')
async def show_portfolio_alalytics(callback: CallbackQuery):
    pass