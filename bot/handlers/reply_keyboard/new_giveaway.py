from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.state.states_initialization import NewGiveAway
from logs.logger import logger

router = Router()


@router.message(F.text == "🎁Создать розыгрыш🎁")
async def create_giveaway(message: types.Message, state: FSMContext):
    try:
        await message.answer(text="Введите текст поста:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(NewGiveAway.give_post_text)
    except Exception as e:
        logger.error("Возникла ошибка в create_giveaway: %s", e)
