from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from bot.state.states_initialization import NewOrder
from bot.handlers.messages.start import start
from bot.utils.request_to_admin.request_to_admin import send_request_to_admin
from database.database_code import Database
from logs.logger import logger

router = Router()

db = Database()


@router.message(NewOrder.give_customer)
async def give_customer(message: types.Message, state: FSMContext):
    try:
        if message.text:
            await state.update_data(customer_name=message.text.replace("\n", " ").strip())
            await message.answer(text="Отлично! Теперь введите номер телефона, он должен начинаться с '8':")
            await state.set_state(NewOrder.give_phone)
        else:
            await message.answer(text="Отправьте текст!")
    except Exception as e:
        logger.error("Возникла ошибка в give_customer: %s", e)


@router.message(NewOrder.give_phone)
async def give_phone(message: types.Message, state: FSMContext):
    try:
        if message.text.startswith("+8") or message.text.startswith("8"):
            await state.update_data(phone_number=message.text.replace("\n", " ").strip())
            await message.answer(text="Отлично!Теперь введите ваше ФИО:")
            await state.set_state(NewOrder.give_fullname)
        else:
            await message.answer("Номер должен начинаться с '8'!")
    except Exception as e:
        logger.error("Возникла ошибка в give_phone: %s", e)


@router.message(NewOrder.give_fullname)
async def give_fullname(message: types.Message, state: FSMContext):
    try:
        await state.update_data(fullname=message.text)
        await message.answer(text="Теперь введите кол-во покупок:")
        await state.set_state(NewOrder.give_amount)
    except Exception as e:
        logger.error("Возникла ошибка в give_fullname: %s", e)


@router.message(NewOrder.give_amount)
async def give_amount(message: types.Message, state: FSMContext):
    try:
        if message.text and message.text.isdigit():
            state_data = await state.get_data()

            await send_request_to_admin(customer_name=state_data["customer_name"],
                                        phone=state_data["phone_number"], fullname=state_data["fullname"],
                                        amount_of_orders=message.text.replace("\n", " ").strip(),
                                        user_id=message.chat.id)

            await message.answer("Ваша заявка на участие в конкурсе отправлена администратору!\n"
                                 "Ожидайте ответа.")
        else:
            await message.answer("Отправьте мне целое число!")
            return
    except Exception as e:
        logger.error("Возникла ошибка в give_amount: %s", e)
    finally:
        await state.clear()
        await start(message=message)

