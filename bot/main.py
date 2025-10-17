import asyncio
from aiogram import Dispatcher
from bot.bot_instance import bot
from bot.including_routers.main_router import include_all_routers
from bot.utils.check_giveaways.check_giveaways import periodic_update
from database.database_code import Database
from logs.logger import logger

dp = Dispatcher()

db = Database()


async def init_bot():
    logger.debug('Бот был спроектирован и создан Владимиром (https://kwork.ru/user/maket14).')
    logger.warning(
        'Настоящее авторское право принадлежит только мне, копирование и присваивание любых фрагментов кода и проекта в целом без разрешения не допускается.')
    logger.debug('Подготовка к запуску')

    # Создание таблиц в базе данных
    db.create_tables()

    logger.debug('Запуск бота')
    logger.info('Бот запущен!')


async def main():
    await init_bot()
    include_all_routers(dp=dp)
    await asyncio.gather(dp.start_polling(bot), periodic_update())

