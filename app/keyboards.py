from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_classes, get_class_teacher


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Классные руководители'), KeyboardButton(text='Кабинеты')],
        [KeyboardButton(text='Расписание класса'), KeyboardButton(text='Расписание учителя')],
        [KeyboardButton(text='Замены')]
        # [KeyboardButton(text='Замены'), KeyboardButton(text='Время')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...'
)


# async def classes():
#     all_classes = await get_classes()
#     keyboard = InlineKeyboardBuilder()
#
#     for class_item in all_classes:
#         keyboard.add(
#             InlineKeyboardButton(
#                 text=class_item.class_nl,
#                 callback_data=f"class_{class_item.class_nl}"
#             )
#         )
#
#     return keyboard.adjust(2).as_markup()

