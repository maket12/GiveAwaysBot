from aiogram import Router, types, Bot
from aiogram.filters.command import CommandStart
from bot.keyboards.buttons import admin_markup, main_menu_markup, main_admin_markup
from bot.config import admin_ids, main_admin_id
from logs.logger import logger


router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    # Получаем аргументы из команды /start
    args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

    # Проверка и обработка параметра client_id
    if 'client_id=' in args:
        client_id = args.split('client_id=')[1]
        await message.answer(f"Получен client_id: {client_id}")
    else:
        await message.answer(f"Переданы аргументы: {args}")
