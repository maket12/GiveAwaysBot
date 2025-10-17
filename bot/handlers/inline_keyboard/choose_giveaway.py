from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.bot_instance import bot
from bot.state.states_initialization import NewGiveawayDate
from database.database_code import Database
from logs.logger import logger

router = Router()

db = Database()


@router.callback_query(F.data.startswith("giveaway"))
async def choose_giveaway(call: types.CallbackQuery, state: FSMContext):
    try:
        giveaway_id = call.data.split("_")[1]

        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text="Отправьте новую дату для этого розыгрыша\n"
                                                               "Формат следующий: день.месяц.год час:минута\n"
                                                               "Пример: 29.07.2024 15:16")
        await state.set_state(NewGiveawayDate.give_new_date)
        await state.update_data(giveaway_id=giveaway_id)
    except Exception as e:
        logger.error("Возникла ошибка в choose_giveaway: %s", e)

