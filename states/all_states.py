from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

class FeedbackState(StatesGroup):
    get_feedback = State()


class MenuState(StatesGroup):
    menu = State()


class SearchCoins(StatesGroup):
    search_coins = State()
    coins_amount = State()


class AnalysisCoin(SearchCoins):
    search_coin_for_analys = State()


class EmailInput(StatesGroup):
    check_email = State()


class Filters(StatesGroup):
    trading_volume = State()
    exchange = State()
    volatility = State()
    show_results = State()

