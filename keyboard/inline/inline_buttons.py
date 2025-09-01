from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def portfolio_button():
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕ Добавить актив', callback_data='add_asset')],
        [InlineKeyboardButton(text='📊 Статистика', callback_data='show_statistics')],
        [InlineKeyboardButton(text='↩️ Назад', callback_data='go_menu')]
    ])
    return button


def menu_button():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text='💰 Мой портфель', callback_data='portfolio_button'),
                InlineKeyboardButton(text='📈 Аналитика', callback_data='show_analytics'),
                InlineKeyboardButton(text='🔍 Идеи', callback_data='show_ideas'),
                InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings_button'),
                InlineKeyboardButton(text='ℹ️ Помощь', callback_data='help_button'))


    builder.adjust(1, 1, 1, 2)
    return builder.as_markup()


def settings_button():
    notifications = ['✅', '❌']

    builder = InlineKeyboardBuilder()
    currencies = ["USD", "EUR", "RUB", "GBP", "BTC", "ETH", "CNY", "JPY"]

    for currency in currencies:
        builder.add(InlineKeyboardButton(text=f'{currency}', callback_data=f'currency_{currency}'))

    builder.add(InlineKeyboardButton(text=f'Уведомления {notifications[0]}', callback_data='notifications_button'))
    builder.add(InlineKeyboardButton(text='Привязать email', callback_data='email_button'))
    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data='go_menu'))

    builder.adjust(4, 4, 1, 1, 1)
    return builder.as_markup()


def help_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Сообщить об ошибке / Оставить отзыв', callback_data='feedback_button'))
    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data='go_menu'))

    builder.adjust(1, 1)
    return builder.as_markup()


def top_coins_buttons(coins_list: list):
    builder = InlineKeyboardBuilder()
    for coin in coins_list:
        builder.add(InlineKeyboardButton(text=f'{coin[2]}|{coin[1]}', callback_data=f'AddCoin_{coin[0]}'))

    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data='go_menu'))

    builder.adjust(2, 2, 2, 2, 2, 1)
    return builder.as_markup()


def show_ideas_buttons(coins_list: list):
    builder = InlineKeyboardBuilder()
    for coin in coins_list:
        builder.add(InlineKeyboardButton(text=f'{coin[2]}|{coin[1]}', callback_data=f'CoinAnalysis_{coin[0]}'))

    builder.add(InlineKeyboardButton(text='Фильтры для поиска', callback_data='use_filters'))
    builder.add(InlineKeyboardButton(text='Скачать отчеты', callback_data='download_file_top'))
    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data='go_menu'))

    builder.adjust(4, 4, 4, 1, 1, 1)
    return builder.as_markup()


def add_new_coin_button(coin_id: str):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text='Добавить в портфель', callback_data=f'AddCoin_{coin_id}'))
    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data='go_menu'))

    builder.adjust(1, 1)
    return builder.as_markup()


def go_back_button():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data='go_menu'))
    return builder.as_markup()


def show_search_results_buttons(coins_list: list):
    builder = InlineKeyboardBuilder()
    for coin in coins_list:
        builder.add(InlineKeyboardButton(text=f'{coin[2]}|{coin[1]}', callback_data=f'CoinAnalysis_{coin[0]}'))

    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data='go_menu'))

    builder.adjust(1)
    return builder.as_markup()
