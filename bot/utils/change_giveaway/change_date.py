from bot.bot_instance import bot
from bot.utils.create_text.create_giveaway_text import create_text
from bot.utils.datetime_utils import time_to_date
from bot.config import channel_id
from database.database_code import Database
from logs.logger import logger

db = Database()


async def change_date_in_channel(giveaway_id: int):
    try:
        giveaway_data = db.get_giveaway_by_id(giveaway_id=giveaway_id)
        giveaway_id, post_text, post_photo, prizes, amount_of_orders, finish_date, post_id = giveaway_data
        data_for_text = [post_text, post_photo, prizes, amount_of_orders, time_to_date(finish_date)]
        giveaway_text = await create_text(data_for_text)
        await bot.edit_message_caption(chat_id=channel_id, message_id=post_id, caption=giveaway_text)
    except Exception as e:
        logger.error("Возникла ошибка в change_date_in_channel: %s", e)
