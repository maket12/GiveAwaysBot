from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from bot.state.states_initialization import NewGiveawayDate
from bot.utils.change_giveaway.change_date import change_date_in_channel
from bot.utils.datetime_utils import string_to_time
from database.database_code import Database
from logs.logger import logger

router = Router()

db = Database()


@router.message(NewGiveawayDate.give_new_date)
async def give_new_date(message: types.Message, state: FSMContext):
    try:
        if ":" in message.text and "." in message.text:
            state_data = await state.get_data()
            giveaway_id = state_data["giveaway_id"]

            new_date = string_to_time(message.text.strip())
            db.set_new_date(giveaway_id=giveaway_id, date=new_date)

            await change_date_in_channel(giveaway_id=giveaway_id)
            await message.answer(text="Дата успешно изменена!")
        else:
            await message.answer("Неверный формат даты! Повторите ещё раз!")
            return
    except Exception as e:
        logger.error("Возникла ошибка в give_new_date: %s", e)
    finally:
        await state.clear()
