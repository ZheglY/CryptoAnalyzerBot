from db.models import async_session
from api.coingecko_api import get_top_coins
from utils.logger import get_logger

from api.coingecko_api import get_coin_price, get_coin_details, get_coin_price
from db.crud import change_or_get_currency, get_user_balance


logger = get_logger(__name__)

async def show_portfolio(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            response = dict()
            response['total_price'] = 0

            balance = await get_user_balance(tg_id=tg_id, session=session)
            currency = await change_or_get_currency(tg_id=tg_id, session=session)
            response['currency'] = currency

            for coin in balance:
                coin_price = int(await get_coin_price(coin_id=coin[0], currency=currency))
                response['total_price'] += coin_price

            return response
# функция Текущая стоимость  current_balance = user_balance(session, tg_id)
# функция Изменение за 24ч:  тут ваще хз что
# функция Распределение по активам  тут должна быть какая то функция


async def show_top_coins_service(tg_id: int, limit: int):
    async with async_session() as session:
        async with session.begin():
            user_currency = await change_or_get_currency(session=session, tg_id=tg_id) # тут вернется валюта RUB, USD
            logger.info(f'Текущая валюта {user_currency} | portfolio_add_coins')

            top_coins = await get_top_coins(user_currency.lower(), limit)  # возвращается лист имен для кнопок
            coins_names = [(coin['id'], coin['symbol'].upper(), coin['name']) for coin in top_coins]
            return coins_names


async def add_coin_info(coin_id: str, tg_id: int):
    async with async_session() as session:
        async with session.begin():
            currency = await change_or_get_currency(session=session, tg_id=tg_id)  # валюта пользователя
            coin_price = await get_coin_price(coin_id, currency)  # стоимость одной монеты

            response = await get_coin_details(coin_id) # получение имени
            if response['name']:
                coin_name = response['name']

            return coin_name, coin_price, currency


