from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Кнопки главного меню

main_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="Принять участие в розыгрыше")
    ]
])


# Кнопки админ меню

admin_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="🎁Создать розыгрыш🎁")
    ],
    [
        KeyboardButton(text="Принять участие в розыгрыше")
    ]
])


# Кнопки меню главного админа

main_admin_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="Удалить клиента")
    ],
    [
        KeyboardButton(text="Изменить дату розыгрыша")
    ]
])


# Кнопка стоп при прекреплении фото

stop_adding_photo_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="Больше нет фото")
    ]
])


# Кнопка стоп при прекреплении призов

stop_adding_prizes_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="Больше нет призов")
    ]
])


# Кнопки подтвердить/отклонить участие в розыгрыше

async def create_participating_answers_markup(user_id: int):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить✅", callback_data=f"accept_{user_id}")
        ],
        [
            InlineKeyboardButton(text="Отклонить❌", callback_data=f"reject_{user_id}")
        ]
    ])
    return markup


# Кнопки выбора розыгрыша

async def create_giveaways_markup(giveaways_data: list):
    markup = InlineKeyboardBuilder()
    buttons = []
    for giveaway in giveaways_data:
        buttons.append(InlineKeyboardButton(text=f"Розыгрыш от {giveaway[1]}",
                                            callback_data=f"giveaway_{giveaway[0]}"))
    markup.add(*buttons)
    return markup.adjust(1).as_markup()

