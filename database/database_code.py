import sqlite3
import os
from logs.logger import logger


class Database:
    def __init__(self, db_file="database.db"):

        # Получаем абсолютный путь к файлу базы данных относительно этого файла
        base_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(base_dir, db_file)

        self.connection = sqlite3.connect(absolute_path)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            try:
                logger.debug('Подключение к базе данных')
                self.cursor.execute('CREATE TABLE IF NOT EXISTS "giveaways" ('
                                    '"id" INTEGER PRIMARY KEY AUTOINCREMENT, '
                                    '"post_text" TEXT,'
                                    '"post_photo" TEXT,'
                                    '"prizes" TEXT,'
                                    '"amount_of_orders" INTEGER,'
                                    '"finish_date" INTEGER,'
                                    '"message_id" INTEGER)')

                logger.info('База данных розыгрышей подключена успешно!')

                self.cursor.execute('CREATE TABLE IF NOT EXISTS "customers" ('
                                    '"id" INTEGER PRIMARY KEY AUTOINCREMENT,'
                                    '"name" TEXT,'
                                    '"phone_number" TEXT,'
                                    '"amount_of_orders" INTEGER DEFAULT 0)')

                logger.info('База данных покупателей подключена успешно!')

                logger.debug('База данных подключена успешно')
            except Exception as e:
                logger.error(f'Ошибка при подключении к базе данных: {e}')

    def customer_exists(self, customer_phone: str):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM "customers" WHERE "phone_number" = ?',
                                         (customer_phone,)).fetchmany(1)
            return bool(len(result))

    def add_customer(self, customer_data: list):
        with self.connection:
            return self.cursor.execute('INSERT INTO "customers" '
                                       '("name", "phone_number", "amount_of_orders") '
                                       'VALUES (?, ?, ?)', customer_data)

    def set_amount(self, phone_number: str, amount_of_orders: int):
        with self.connection:
            return self.cursor.execute('UPDATE "customers" SET "amount_of_orders" = ? '
                                       'WHERE "phone_number" = ?',
                                       (amount_of_orders, phone_number))

    def set_new_date(self, giveaway_id: int, date: int):
        with self.connection:
            return self.cursor.execute('UPDATE "giveaways" SET "finish_date" = ? WHERE "id" = ?',
                                       (date, giveaway_id))

    def add_giveaway(self, giveaway_data: list):
        with self.connection:
            return self.cursor.execute('INSERT INTO "giveaways" ("post_text", "post_photo", '
                                       '"prizes", "amount_of_orders", "finish_date", "message_id") VALUES '
                                       '(?, ?, ?, ?, ?, ?)', giveaway_data)

    def get_giveaways(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM "giveaways"').fetchall()

    def get_giveaway_by_id(self, giveaway_id: int):
        with self.connection:
            return self.cursor.execute('SELECT * FROM "giveaways" WHERE "id" = ?',
                                       (giveaway_id,)).fetchone()

    def get_customers(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM "customers"').fetchall()

    def get_amount_of_orders(self, customer_name: str):
        with self.connection:
            return self.cursor.execute('SELECT "amount_of_orders" FROM "customers" WHERE "name" = ?',
                                       (customer_name,)).fetchone()[0]

    def delete_customer(self, phone_number: str):
        with self.connection:
            return self.cursor.execute('DELETE FROM "customers" WHERE "phone_number" = ?',
                                       (phone_number,))

    def delete_all_customers(self):
        with self.connection:
            return self.cursor.execute('DELETE FROM "customers"')

    def delete_giveaway(self, giveaway_id: int):
        with self.connection:
            return self.cursor.execute('DELETE FROM "giveaways" WHERE "id" = ?',
                                       (giveaway_id,))

