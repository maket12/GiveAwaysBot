from aiogram.utils.media_group import MediaGroupBuilder
from bot.bot_instance import bot
from bot.utils.create_text.create_giveaway_text import create_text
from bot.config import channel_id
from logs.logger import logger


async def upload_giveaway(giveaway_data: list):
    try:
        post_photo = giveaway_data[1]
        text = await create_text(giveaway_data=giveaway_data)

        photos = post_photo.split("|")
        if len(photos) == 1:
            sent_message = await bot.send_photo(chat_id=channel_id, photo=photos[0],
                                                caption=text, parse_mode='html')
            message_id = sent_message.message_id
        else:
            media_group = MediaGroupBuilder(caption=text)

            for photo in photos:
                media_group.add_photo(media=photo)

            sent_message = await bot.send_media_group(chat_id=channel_id,
                                                      media=media_group.build())

            message_id = sent_message[0].message_id

        await bot.pin_chat_message(chat_id=channel_id, message_id=message_id)

        return message_id
    except Exception as e:
        logger.error("Возникла ошибка в upload_giveaway: %s", e)
