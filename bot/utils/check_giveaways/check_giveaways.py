import asyncio
import time
from bot.services.random_org.get_random_value import get_random_value
from bot.utils.giveaway_results.update_results import update_giveaway_results
from database.database_code import Database
from logs.logger import logger

db = Database()


async def periodic_update():
    while True:
        try:
            await asyncio.sleep(5)  # Пауза 2 минуты

            all_giveaways = db.get_giveaways()
            for giveaway in all_giveaways:
                if giveaway[5] <= int(time.time()):  # Если время пришло
                    all_customers = db.get_customers()
                    participants = []
                    winners = []

                    for customer in all_customers:
                        amount_of_coupons = customer[3] // giveaway[4]
                        if amount_of_coupons > 0:
                            # Добавляем столько раз, сколько купонов
                            for i in range(amount_of_coupons):
                                participants.append(customer)

                    for count in range(len(giveaway[3].split(', '))):
                        winner = await get_random_value(values=participants)

                        # Удаляем все вхождения в список
                        while winner in participants:
                            participants.remove(winner)

                        winners.append(winner)

                    db.delete_giveaway(giveaway_id=giveaway[0])  # Удаляем розыгрыш из БД
                    db.delete_all_customers()  # Чистим таблицу участников

                    await update_giveaway_results(giveaway_message_id=giveaway[6], winners=winners)
                    break
        except Exception as e:
            logger.error("Возникла ошибка в periodic_update: %s", e)
            await asyncio.sleep(300)
