from aiogram import Router, types, F
from bot.utils.datetime_utils import time_to_date
from bot.keyboards.buttons import create_giveaways_markup
from logs.logger import logger
from database.database_code import Database

router = Router()

db = Database()


@router.message(F.text == "Изменить дату розыгрыша")
async def get_new_date(message: types.Message):
    try:
        giveaways = db.get_giveaways()
        giveaways_data = []

        for giveaway in giveaways:
            giveaways_data.append([giveaway[0], time_to_date(giveaway[5])])

        await message.answer(text="Выберите дату какого розыгрыша необходимо изменить:",
                             reply_markup=await create_giveaways_markup(giveaways_data=giveaways_data))
    except Exception as e:
        logger.error("Возникла ошибка в get_new_date: %s", e)
