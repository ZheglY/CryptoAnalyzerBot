from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputFile, BufferedInputFile
from keyboard.inline.inline_buttons import add_new_coin_button, go_back_button, show_search_results_buttons
from api.coingecko_api import get_coin_details, get_top_coins
from services.analysis_coin_service import show_top_coins_service, show_search_results, download_reports
from states.all_states import AnalysisCoin
from handlers.commands.base_commands import show_profile_command
from utils.string_math_utils import change_data_format

analysis_router = Router()


@analysis_router.callback_query(F.data == 'show_analytics')
async def analysis_coin_menu_handler(callback: CallbackQuery, state:FSMContext):
    """Хендлер отображает меню Аналитика при нажатии кнопки"""
    text = ('Введите название монеты для анализа в таком формате (BTC)')

    await callback.message.answer(text, reply_markup=go_back_button())
    await callback.answer()

    await state.set_state(AnalysisCoin.search_coin_for_analys)


@analysis_router.message(AnalysisCoin.search_coin_for_analys)
async def show_coin_search_handler(message: Message, state:FSMContext):
    """Хендлер отображает найденные коины по запросу пользователя"""
    result = await show_search_results(message.text,10)
    coin_info = change_data_format(result) # меняет формат информации для создания кнопок

    text = (f'Найденные по запросу монеты: \n\n')
    await message.answer(text, reply_markup=show_search_results_buttons(coin_info))

    await state.clear()


@analysis_router.callback_query(lambda c: c.data.startswith('CoinAnalysis'))
async def analysis_coin_handler(callback: CallbackQuery):
    """Хендлер получает айди коина для полного анализа монеты"""
    coin_id = callback.data.split('_')[1]
    text, image = await show_top_coins_service(tg_id=callback.from_user.id, coin_id=coin_id)

    if image:
        await callback.message.answer_photo(
            photo=image,
        )
    await callback.message.answer(text, reply_markup=add_new_coin_button(coin_id))
    await callback.answer()
    # добавить кнопку скачать инфо как csv


@analysis_router.callback_query(F.data == 'download_file_top')   # доделать!!
async def analysis_download_files(callback: CallbackQuery):
    """Хендлер для скачивания файла"""
    text = 'Здесь можно скачать файл в формате CSV / txt'
    await callback.message.answer(text, reply_markup=go_back_button())
    await callback.answer()

    tg_id = callback.from_user.id
    file_txt, csv_file = await download_reports(tg_id)

    await callback.message.answer_document(
        document=BufferedInputFile(
            file=file_txt.getvalue(),
            filename=f"crypto_report_{datetime.now().strftime('%Y-%m-%d %H:%M')}.txt"
        ),
    )
    await callback.message.answer_document(
        document=BufferedInputFile(
            file=csv_file,
            filename=f"crypto_report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
        ),
    )

