from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.state.states_initialization import DeleteCustomer
from logs.logger import logger


router = Router()


@router.message(F.text == "Удалить клиента")
async def change_amount(message: types.Message, state: FSMContext):
    try:
        await message.answer(text="Хорошо, введите номер телефона клиента:")
        await state.set_state(DeleteCustomer.give_phone)
    except Exception as e:
        logger.error("Возникла ошибка в change_amount: %s", e)
