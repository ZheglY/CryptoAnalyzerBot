from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from utils.logger import get_logger
from aiogram.types import CallbackQuery, Message
from api.coingecko_api import get_top_coins
from services.portfolio_service import show_top_coins_service
from keyboard.inline.inline_buttons import show_ideas_buttons
from states.all_states import Filters
from services.ideas_service import find_coins_by_filters



ideas_router = Router()
logger = get_logger(__name__)


@ideas_router.callback_query(F.data == 'show_ideas')
async def show_ideas_menu(callback: CallbackQuery):
    text = ('Здесь вы можете найти новую монету для своего портфеля! Выберите монету из топ 20 самых популярных снизу'
            'или воспользуйтесь фильтрами для поиска!\n\n'
            'Вы можете скачать CSV или txt файл где найдете топ 100 монет с информацией о каждой')

    coins_list = await show_top_coins_service(callback.from_user.id, limit=12)
    print(coins_list)
    await callback.message.answer(text, reply_markup=show_ideas_buttons(coins_list))
    await callback.answer()

#---------------------------------------------------------------------------

@ideas_router.callback_query(F.data == 'use_filters') # work
async def price_filter_handler(callback: CallbackQuery, state:FSMContext):
    text = ('Для поиске необходимо будет последовательно вводить 5 основных фильтров. \т'
            'Если вы хотите пропустить фильтр просто укажите знак минуса "-"\n\n'
            '💰 Ценовой диапазон ($) Укажите минимальную и максимальную цену через пробел (например: 0.1 5):')

    await state.set_state(Filters.trading_volume)
    await callback.message.answer(text)
    await callback.answer()


@ideas_router.message(Filters.trading_volume) # work
async def trading_volume_handler(message: Message, state:FSMContext):
    text = 'Минимальный объем торгов за 24ч (например: 1000000 для $1M):'

    await state.update_data(price=message.text)
    await state.set_state(Filters.exchange)
    await message.answer(text)


@ideas_router.message(Filters.exchange) # work
async def exchange_filter_handler(message: Message, state:FSMContext):
    text = "Выберите биржу из списка: Binance, Coinbase, Kraken, OKX (или введите 'любая'):"

    await state.update_data(trading=message.text)
    await state.set_state(Filters.volatility)
    await message.answer(text)


@ideas_router.message(Filters.volatility) # work
async def volatility_filter_handler(message: Message, state:FSMContext):
    text = "Укажите уровень волатильности: Низкая, Средняя, Высокая (или 'любая'):"

    await state.update_data(exchange=message.text)
    await state.set_state(Filters.show_results)
    await message.answer(text)


@ideas_router.message(Filters.show_results) # work
async def volatility_filter_handler(message: Message, state:FSMContext):
    text = "Результаты поиска по указанным фильтрам"

    filters = await state.get_data()

    price = filters.get('price')
    trading = filters.get('trading')
    exchange = filters.get('exchange')
    volatility = message.text

    all_filters = (price, trading, exchange, volatility)
    await find_coins_by_filters(all_filters=all_filters, tg_id=message.from_user.id)

    await state.clear()
    await message.answer(text)