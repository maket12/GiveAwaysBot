from logs.logger import logger


async def create_text(giveaway_data: list):
    try:
        post_text, post_photo, prizes, amount_of_orders, finish_date = giveaway_data

        text = post_text + "\n➖➖➖➖➖➖➖➖\nПризы:"

        count = 0
        for prize in prizes.split(', '):
            count += 1
            text += f"\n{count} место - {prize.capitalize()}"

        text += (f"\n➖➖➖➖➖➖➖➖\n"
                 f"Количество покупок для получения 1 купона на участие: {amount_of_orders}\n"
                 f"🗓Дата розыгрыша: {finish_date}")

        return text
    except Exception as e:
        logger.error("Возникла ошибка в create_text: %s", e)
