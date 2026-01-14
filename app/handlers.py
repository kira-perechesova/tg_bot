from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        'Здравствуйте!\nЯ бот, созданный президентом гимназии №24 в 2026 году.',
        reply_markup=kb.main
    )


@router.message(F.text == 'Классные руководители')
async def classes(message: Message):
    await message.answer(
        'Выберите класс',
        reply_markup=await kb.classes()
    )


@router.callback_query(F.data.startswith('class_'))
async def show_class_teacher(callback: CallbackQuery):
    class_nl = callback.data.split('_')[1]

    await callback.answer()

    teacher = await rq.get_class_teacher(class_nl)

    if not teacher:
        await callback.message.answer(
            f'Для класса {class_nl} классный руководитель не найден'
        )
        return

    await callback.message.answer(
        f'Классный руководитель {class_nl}:\n'
        f'{teacher.name}'
    )
