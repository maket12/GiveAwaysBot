from bot.bot_instance import bot
from bot.config import channel_id
from logs.logger import logger


async def update_giveaway_results(giveaway_message_id: int, winners: list):
    try:
        message_text = "🎉Результаты розыгрыша🎉:"
        count = 0

        for winner in winners:
            count += 1
            message_text += f"\n{count} место - {winner[1]}({winner[2]})"

        message_text += "\nВсем спасибо за участие💚"

        await bot.send_message(chat_id=channel_id, text=message_text,
                               reply_to_message_id=giveaway_message_id)
        await bot.unpin_chat_message(chat_id=channel_id, message_id=giveaway_message_id)
    except Exception as e:
        logger.error("Возникла ошибка в update_giveaway_results: %s", e)
