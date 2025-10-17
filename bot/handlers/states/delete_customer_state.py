from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from bot.state.states_initialization import DeleteCustomer
from bot.handlers.messages.start import start
from database.database_code import Database
from logs.logger import logger

router = Router()

db = Database()


@router.message(DeleteCustomer.give_phone)
async def give_phone_number(message: types.Message, state: FSMContext):
    try:
        if message.text.startswith("+8") or message.text.startswith("8"):
            db.delete_customer(phone_number=message.text)
            await message.answer("Покупатель успешно удалён!")
            await start(message=message)
        else:
            await message.answer(text="Отправьте номер, который начинается с цифры '8'!")
            return
    except Exception as e:
        logger.error("Возникла ошибка в give_phone_number: %s", e)
    finally:
        await state.clear()
