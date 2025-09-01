from db.models import async_session
from api.coingecko_api import get_top_coins
from utils.logger import get_logger

from api.coingecko_api import get_coin_price, get_coin_details
from db.crud import change_or_get_currency


async def find_coins_by_filters(all_filters, tg_id: int):
    pass