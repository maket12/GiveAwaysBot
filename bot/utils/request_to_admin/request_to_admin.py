from aiogram.exceptions import TelegramBadRequest
from bot.bot_instance import bot
from bot.config import admin_ids
from bot.keyboards.buttons import create_participating_answers_markup
from logs.logger import logger


async def send_request_to_admin(customer_name: str, phone: str, fullname: str, amount_of_orders: str, user_id: int):
    try:
        user = await bot.get_chat(user_id)
        for admin_id in admin_ids:
            try:
                await bot.send_message(chat_id=admin_id, text="Пришла новая заявка на участие в конкурсе:\n"
                                                              f"Имя: {customer_name}\n"
                                                              f"Номер телефона: {phone}\n"
                                                              f"ФИО: {fullname}\n"
                                                              f"Количество заказов: {amount_of_orders}\n"
                                                              f"Контакты: @{user.username}",
                                       reply_markup=await create_participating_answers_markup(user_id))
            except TelegramBadRequest:
                pass
    except Exception as e:
        logger.error("Возникла ошибка в send_request_to_admin: %s", e)

