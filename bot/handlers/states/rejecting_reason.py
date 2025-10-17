from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from bot.bot_instance import bot
from bot.state.states_initialization import RejectingReason
from logs.logger import logger

router = Router()


@router.message(RejectingReason.give_reason)
async def give_rejecting_reason(message: types.Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        user_id = state_data["user_id"]

        await bot.send_message(chat_id=user_id, text="Ваша заявка на участие в розыгрыше отменена!\n"
                                                     f"Причина: {message.text}")

        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id, text="Заявка отклонена.")
    except Exception as e:
        logger.error("Возникла ошибка в give_rejecting_reason: %s", e)

