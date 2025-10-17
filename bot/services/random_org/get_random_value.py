import requests
from bot.config import random_api_token
from logs.logger import logger


async def get_random_value(values: list):
    try:
        # Формируем запрос к API
        url = 'https://api.random.org/json-rpc/4/invoke'
        headers = {'Content-Type': 'application/json'}
        payload = {
            'jsonrpc': '2.0',
            'method': 'generateIntegers',
            'params': {
                'apiKey': random_api_token,
                'n': 1,  # Количество случайных чисел
                'min': 0,
                'max': len(values) - 1,  # Индекс последнего элемента в списке
                'replacement': False
            },
            'id': 1
        }

        # Отправка запроса и получение случайного индекса
        response = requests.post(url, headers=headers, json=payload)
        print(response.json())
        random_index = response.json()['result']['random']['data'][0]

        # Получение случайного числа из списка
        random_number = values[random_index]
        return random_number
    except Exception as e:
        logger.error("Возникла ошибка в get_random_value: %s", e)

