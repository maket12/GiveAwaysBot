from aiogram import Router, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.state.states_initialization import NewGiveAway
from bot.utils.upload_giveaway.upload_giveaway_in_channel import upload_giveaway
from bot.keyboards.buttons import stop_adding_photo_markup
from bot.utils.datetime_utils import string_to_time
from database.database_code import Database
from logs.logger import logger

router = Router()

db = Database()


@router.message(NewGiveAway.give_post_text)
async def give_post_text(message: types.Message, state: FSMContext):
    try:
        if message.text:
            await state.update_data(post_text=message.text)

            await message.answer(text="Отлично, теперь отправьте фото поста\n"
                                      "Это могут быть фото призов, или описание")

            await state.set_state(NewGiveAway.give_post_photo)
        else:
            await message.answer(text="Отправьте мне текс поста с розыгрышем!")
    except Exception as e:
        logger.error("Возникла ошибка в give_post_text: %s", e)


@router.message(NewGiveAway.give_post_photo)
async def give_post_photo(message: types.Message, state: FSMContext):
    try:
        if message.photo:
            state_data = await state.get_data()
            try:
                current_photos = state_data["post_photo"]
            except:
                current_photos = None

            if not current_photos:
                current_photos = message.photo[-1].file_id
            else:
                current_photos += "|" + message.photo[-1].file_id

            await state.update_data(post_photo=current_photos)

            await message.answer(text="Отправьте ещё фото, если есть\n"
                                      "Если хотите остановиться, нажмите 'Больше нет фото'",
                                 reply_markup=stop_adding_photo_markup)

        elif message.text == "Больше нет фото":
            await message.answer(text="Теперь определимся с призами\n"
                                      "Отправьте призы по порядку через запятую+пробел, "
                                      "в соответствии с их номиналом\n"
                                      "То есть, 1 приз, 2 приз, 3 приз и т.д.",
                                 reply_markup=ReplyKeyboardRemove())

            await state.set_state(NewGiveAway.give_post_prizes)
        else:
            await message.answer(text="Отправьте мне фото!")
    except Exception as e:
        logger.error("Возникла ошибка в give_post_text: %s", e)


@router.message(NewGiveAway.give_post_prizes)
async def give_post_prizes(message: types.Message, state: FSMContext):
    try:
        if message.text:
            await state.update_data(prizes=message.text)

            await message.answer(text="Введите кол-во заказов, которое необходимо для получения 1 купона:")

            await state.set_state(NewGiveAway.give_amount_of_orders)
        else:
            await message.answer(text="Отправьте мне призы в указанном формате!")
    except Exception as e:
        logger.error("Возникла ошибка в give_post_prizes: %s", e)


@router.message(NewGiveAway.give_amount_of_orders)
async def give_amount_of_orders(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            await state.update_data(amount_of_orders=message.text)

            await message.answer(text="Теперь укажите дату розыгрыша\n"
                                      "Формат следующий: день.месяц.год час:минута\n"
                                      "Пример: 29.07.2024 15:16")

            await state.set_state(NewGiveAway.give_post_finish_date)
        else:
            await message.answer("Отправьте целое число!")
    except Exception as e:
        logger.error("Возникла ошибка в give_amount_of_orders: %s", e)


@router.message(NewGiveAway.give_post_finish_date)
async def give_post_finish_date(message: types.Message, state: FSMContext):
    try:
        if message.text and "." in message.text and ":" in message.text:
            state_data = await state.get_data()
            date_to_time = string_to_time(date_string=message.text)

            giveaway_data = [state_data["post_text"], state_data["post_photo"],
                             state_data["prizes"], state_data["amount_of_orders"]]

            # Публикуем в канале анонс розыгрыша
            post_message_id = await upload_giveaway(giveaway_data=giveaway_data + [message.text])
            giveaway_data.append(date_to_time)
            giveaway_data.append(post_message_id)

            db.add_giveaway(giveaway_data=giveaway_data)

            await message.answer(text="Розыгрыш успешно опубликован!")
            await state.clear()
        else:
            await message.answer(text="Отправьте мне дату в указанном формате!")
    except Exception as e:
        logger.error("Возникла ошибка в give_post_finish_date: %s", e)
