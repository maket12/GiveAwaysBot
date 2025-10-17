from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.state.states_initialization import NewOrder
from logs.logger import logger

router = Router()


@router.message(F.text == "Принять участие в розыгрыше")
async def new_order(message: types.Message, state: FSMContext):
    try:
        await message.answer(text="Укажите имя или название заказчика:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(NewOrder.give_customer)
    except Exception as e:
        logger.error("Возникла ошибка в new_order: %s", e)
