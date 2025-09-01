import requests
from aiogram.types import BufferedInputFile
from db.models import async_session
from utils.coin_parser import parse_coin_data, create_txt_report, create_csv_report
from api.coingecko_api import get_coin_price, get_coin_details, get_all_coins, get_top_coins
from db.crud import change_or_get_currency


async def show_top_coins_service(tg_id: int, coin_id: str):
    async with async_session() as session:
        async with session.begin():
            user_currency = await change_or_get_currency(session=session, tg_id=tg_id)
            coin_data = await get_coin_details(coin_id) # api request для информации по конкретной монете
            message_text, image_url = parse_coin_data(data=coin_data, user_currency=user_currency.lower())  #  преобразование api response в текст

            if image_url:
                img_response = requests.get(image_url)
                photo = BufferedInputFile(
                    file=img_response.content,
                    filename=f"{coin_id}.png"
                )
            else:
                photo = None

            return message_text, photo


async def show_search_results(coin_name: str, max_results:5):
    all_coins = await get_all_coins()
    search_query = coin_name.strip().lower()

    exact_symbol_matches = [
        coin for coin in all_coins
        if coin['symbol'].lower() == search_query
    ]

    name_matches = [
        coin for coin in all_coins
        if search_query in coin['name'].lower()
           and coin not in exact_symbol_matches
    ]

    results = exact_symbol_matches + name_matches

    return results[:max_results]


async def download_reports(tg_id):
    async with async_session() as session:
        async with session.begin():
            user_currency = await change_or_get_currency(session=session, tg_id=tg_id)
            top_coins = await get_top_coins(limit=100, currency=user_currency) # получение всех монет API
            file_txt = create_txt_report(top_coins, user_currency=user_currency) # создание тxt файла
            csv_file = create_csv_report(top_coins, user_currency=user_currency)
            return file_txt, csv_file
