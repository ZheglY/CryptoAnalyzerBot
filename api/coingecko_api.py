import aiohttp
from utils.logger import get_logger


logger = get_logger(__name__)



async def get_all_coins():
    """Получение списка всех монет (для ручного ввода)"""
    url = "https://api.coingecko.com/api/v3/coins/list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_top_coins(currency: str, limit: int):
    """Получение топовых монет по капитализации"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency,
        "per_page": limit,
        "sparkline": "false",
        "order": "market_cap_desc"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            logger.info(f'Отправлен API запрос на получение {limit} топовых монет')
            return await response.json()


async def get_coin_details(coin_id: str):
    """Получение деталей по конкретной монете"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    params = {
        'localization': 'true',
        'tickers': 'true',
        'market_data': 'true',
        'community_data': 'true',
        'developer_data': 'true',
        'sparkline': 'false'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url,params=params) as response:
            return await response.json()


async def get_coin_price(coin_id, currency: str):
    """Получение цены конкретной монеты в указанной валюте"""
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": currency,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response = await response.json()
            return response[f'{coin_id}'][f'{currency.lower()}']