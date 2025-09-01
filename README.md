# CryptoAnalyzerBot

🤖 Умный Telegram-бот для анализа и отслеживания криптовалютных активов с расширенной функциональностью.

## ✨ Возможности

- 📊 **Отслеживание курсов** криптовалют в реальном времени
- 📈 **Технический анализ** монет (RSI, Moving Average и др.)
- 💼 **Управление портфелем** - добавление активов и отслеживание PnL
- 💡 **Система идей** - сохранение и анализ торговых идей
- ⚡ **Асинхронная обработка** запросов с помощью aiogram 3.x
- 📝 **Логирование** всех операций
- 🗃️ **Работа с базой данных** SQLite через SQLAlchemy
- 🌐 **Интеграция с CoinGecko API**

## 🏗️ Структура проекта
```
CryptoAnalyzerBot/
├── api/ # Модуль работы с внешними API
│ ├── coingecko_api.py # Клиент для CoinGecko API
│ └── init.py
├── config/ # Конфигурационные файлы
│ ├── bot_config.py # Настройки бота
│ ├── logger_config.py # Конфигурация логгера
│ └── init.py
├── db/ # Модуль работы с базой данных
│ ├── models.py # SQLAlchemy модели
│ ├── crud.py # CRUD операции
│ ├── init_db.py # Инициализация БД
│ └── init.py
├── handlers/ # Обработчики сообщений
│ ├── commands/ # Базовые команды
│ │ └── base_commands.py
│ ├── custom_handlers/ # Специализированные обработчики
│ │ ├── analysis_handlers.py # Анализ монет
│ │ ├── portfolio_handlers.py # Управление портфелем
│ │ ├── ideas_handlers.py # Работа с идеями
│ │ ├── settings_handlers.py # Настройки
│ │ ├── feedback_help_handler.py # Обратная связь
│ │ └── special_handlers.py # Специальные обработчики
│ └── init.py
├── keyboard/ # Модуль клавиатур
│ ├── inline/ # Inline-кнопки
│ │ └── inline_buttons.py
│ ├── reply/ # Reply-кнопки
│ └── init.py
├── middleware/ # Промежуточное ПО
│ ├── middleware.py # Мидлвари
│ └── init.py
├── services/ # Бизнес-логика
│ ├── analysis_coin_service.py # Сервис анализа
│ ├── portfolio_service.py # Сервис портфеля
│ ├── ideas_service.py # Сервис идей
│ └── init.py
├── states/ # Состояния FSM
│ ├── all_states.py # Все состояния
│ └── init.py
├── utils/ # Вспомогательные утилиты
│ ├── coin_parser.py # Парсер монет
│ ├── logger.py # Логгер
│ ├── string_math_utils.py # Математические утилиты
│ └── init.py
├── locales/ # Локализации
├── logs/ # Логи приложения
├── main.py # Точка входа
├── requirements.txt # Зависимости
└── db.sqlite3 # База данных SQLite
```

# 🚀 Установка и запуск

1. **Клонирование репозитория**
```bash
git clone https://github.com/ZheglY/CryptoAnalyzerBot.git
cd CryptoAnalyzerBot
```

Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# или
.venv\Scripts\activate     # Windows
Установка зависимостей
```

```bash
pip install -r requirements.txt
```

Настройка конфигурации
Отредактируйте файл config/bot_config.py:

``` python
BOT_TOKEN = "your_bot_token_here"
```

Запуск бота

``` bash
python main.py
```

# 🛠️ Технологический стек

Python 3.12+ - основной язык программирования

Aiogram 3.x - асинхронный фреймворк для Telegram ботов

SQLAlchemy 2.0 - ORM для работы с базой данных

SQLite3 - база данных

Aiohttp - асинхронные HTTP-запросы

Pandas - анализ данных

Logging - система логирования

# 📋 Основные команды бота
/start - начать работу с ботом

/menu - главное меню

/analysis - анализ криптовалют

/portfolio - управление портфелем

/ideas - система идей

/settings - настройки

/help - помощь

# 🔧 Настройка
Перед запуском убедитесь, что в файле config/bot_config.py установлены все необходимые параметры:

``` python
BOT_TOKEN = "YOUR_BOT_TOKEN"  # Токен от @BotFather
ADMIN_IDS = [123456789]       # ID администраторов
```

# 📊 Логирование
Все действия логируются в папку logs/. Настройки логирования можно изменить в config/logger_config.py.

📝 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.

## Contact
- 💬 Telegram: [@progaem_1098](https://t.me/progaem_1098)  
- 📢 Telegram Channel: [IT_Python_ZheglY](https://t.me/IT_Python_ZheglY)  
- 🐙 GitHub: [ZheglY](https://github.com/ZheglY)
