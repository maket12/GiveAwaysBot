from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.bot_instance import bot
from bot.keyboards.buttons import main_menu_markup
from bot.state.states_initialization import RejectingReason
from database.database_code import Database
from logs.logger import logger

router = Router()

db = Database()


@router.callback_query(F.data.startswith("accept"))
async def accept_participating(call: types.CallbackQuery):
    try:
        user_id = call.data.split("_")[1]

        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text="Заявка одобрена.")

        message_text = call.message.text.split("\n")
        customer_name = message_text[1].split(": ")[1]
        phone_number = message_text[2].split(": ")[1]
        amount_of_orders = message_text[4].split(": ")[1]

        if not db.customer_exists(customer_phone=phone_number):
            customer_data = [customer_name, phone_number, amount_of_orders]
            db.add_customer(customer_data=customer_data)
        else:
            db.set_amount(phone_number=phone_number, amount_of_orders=int(amount_of_orders))

        await bot.send_message(chat_id=user_id, text="Отлично! Вы участвуете в розыгрыше!",
                               reply_markup=main_menu_markup)
    except Exception as e:
        logger.error("Возникла ошибка в accept_participating: %s", e)


@router.callback_query(F.data.startswith("reject"))
async def reject_participating(call: types.CallbackQuery, state: FSMContext):
    try:
        user_id = call.data.split("_")[1]
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text="Укажите причину отклонения заявки:")
        await state.set_state(RejectingReason.give_reason)
        await state.update_data(user_id=user_id)
    except Exception as e:
        logger.error("Возникла ошибка в reject_participating: %s", e)
