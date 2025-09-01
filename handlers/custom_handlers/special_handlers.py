from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from utils.logger import get_logger
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.commands.base_commands import menu_command


special_router = Router()
logger = get_logger(__name__)


@special_router.message()
async def echo(message: Message):
    await message.answer("Sorry, but i dont get the idea. Use commands...")

