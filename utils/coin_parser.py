import csv
from datetime import datetime
from io import BytesIO, StringIO
from .logger import get_logger


logger = get_logger(__name__)


def parse_coin_data(data: dict, user_currency: str):
    """Извлечение только нужных полей"""
    try:
        name = data.get('name', 'N/A')
        symbol = data.get('symbol', '?').upper()
        description = data.get('description', {}).get('ru') or data.get('description', {}).get('en',
                                                                                               'No description available')
        market_data = data.get('market_data', {})
        current_price = market_data.get('current_price', {}).get(user_currency, 0)
        market_cap = market_data.get('market_cap', {}).get(user_currency, 0)
        price_change = market_data.get('price_change_percentage_24h', 0)
        circulating_supply = market_data.get('circulating_supply', 0)
        max_supply = market_data.get('max_supply')

        ath_price = market_data.get('ath', {}).get(user_currency, 0)
        ath_date = (market_data.get('ath_date', {}).get(user_currency, '')[:10]
                    if market_data.get('ath_date') else 'N/A')
        atl_price = market_data.get('atl', {}).get(user_currency, 0)
        atl_date = (market_data.get('atl_date', {}).get(user_currency, '')[:10]
                    if market_data.get('atl_date') else 'N/A')

        ticker_info = ""
        if data.get('tickers'):
            first_ticker = data['tickers'][0]
            ticker_price = first_ticker.get('last', 0)
            exchange_name = first_ticker.get('market', {}).get('name', 'unknown exchange')
            ticker_info = (
                "\n🔍 Торговля:\n"
                f"- Последняя цена на {exchange_name}: {ticker_price:,.2f} {user_currency.upper()}\n"
            )

        community_info = "\n👥 Сообщество:\n"
        community_data = data.get('community_data', {})
        if community_data.get('twitter_followers'):
            community_info += f"- Twitter: {community_data['twitter_followers'] / 1e6:.1f}M подписчиков\n"

        developer_data = data.get('developer_data', {})
        if developer_data.get('commit_count_4_weeks'):
            community_info += f"- GitHub: {developer_data['commit_count_4_weeks']} коммитов за месяц\n"

        message = (
            f"{name} ({symbol})\n\n"
            f"📌 Описание:\n\"{description}\"\n\n"

            "💰 Финансы:\n"
            f"- Цена: {current_price:,.2f} {user_currency.upper()}\n"
            f"- Капитализация: {market_cap / 1e12:,.1f} трлн {user_currency.upper()}\n"
            f"- Изменение (24ч): {price_change:+.1f}%\n"
            f"- В обращении: {circulating_supply:,.1f} {symbol}\n"
        )

        if max_supply:
            message += f"- Максимум: {max_supply:,.1f} {symbol}\n"

        message += (
            "\n📈 Исторические данные:\n"
            f"- ATH: {user_currency.upper()} | {ath_price:,.2f} ({ath_date})\n"
            f"- ATL: {user_currency.upper()} | {atl_price:,.2f} ({atl_date})\n"
            f"{ticker_info}"
            f"{community_info if community_info != '\n👥 Сообщество:\n' else ''}"
        )

        image_sizes = data.get('image', {})
        image_url = None

        for size in ['large', 'small', 'thumb']:
            if size in image_sizes:
                image_url = image_sizes[size]
                break

        return message, image_url

    except Exception as e:
        return f"⚠️ Ошибка при обработке данных: {str(e)}"


def create_txt_report(coins_data: dict, user_currency: str):
    """Парсинг данных топовых монет"""
    """Генерирует текстовый файл с данными о криптовалютах"""
    report = BytesIO()

    header = (
        f"Отчет по топовым криптовалютам\n"
        f"Валюта: {user_currency.upper()}\n"
        f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"{'-' * 50}\n\n"
    )
    report.write(header.encode('utf-8'))

    for coin in coins_data:
        coin_info = (
            f"{coin['market_cap_rank']}. {coin['name']} ({coin['symbol'].upper()})\n"
            f"Цена: {coin['current_price']:,.2f} {user_currency.upper()}\n"
            f"Капитализация: {coin['market_cap'] / 1e12:,.1f} трлн {user_currency.upper()}\n"
            f"Изменение (24ч): {coin.get('price_change_percentage_24h', 0):+.1f}%\n"
            f"Обращение: {coin['circulating_supply']:,.1f} {coin['symbol'].upper()}\n"
            f"{'-' * 30}\n\n"
        )
        report.write(coin_info.encode('utf-8'))

    report.seek(0)
    return report


def create_csv_report(coins_data: dict, user_currency: str):
    """Генерирует CSV файл с данными о криптовалютах с правильным форматированием"""
    csv_output = StringIO()

    writer = csv.writer(
        csv_output,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
        lineterminator='\n'
    )

    csv_output.write('\ufeff')

    writer.writerow(['Rank', 'Name', 'Symbol', 'Price', 'Market Cap', '24h Change'])

    for coin in coins_data:
        writer.writerow([
            coin.get('market_cap_rank', 'N/A'),
            coin.get('name', 'N/A'),
            coin.get('symbol', 'N/A').upper(),
            f"{coin.get('current_price', 0):,.2f} {user_currency.upper()}",
            f"{coin.get('market_cap', 0) / 1e12:,.2f} трлн {user_currency.upper()}",
            f"{coin.get('price_change_percentage_24h', 0):+.1f}%"
        ])

    csv_content = csv_output.getvalue().encode('utf-8-sig')
    csv_output.close()

    return csv_content


