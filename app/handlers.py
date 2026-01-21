from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

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

@router.message(F.text == 'Замены')
async def send_zameny(message: Message):
    file = FSInputFile('app/files/замены_на_21.01.2026.jpg')
    await message.answer_document(
        document=file,
        caption='Актуальные замены'
    )

@router.message(F.text == 'Кабинеты')
async def kabinet_start(message: Message):
    await message.answer(
        'Введите номер кабинета (например: 51):'
    )

@router.message(F.text.regexp(r'^\d+$'))
async def kabinet_search(message: Message):
    kabinet_number = int(message.text)

    kabinet = await rq.get_kabinet_by_number(kabinet_number)

    if not kabinet:
        await message.answer(
            f'Кабинет №{kabinet_number} не найден в базе данных'
        )
        return

    await message.answer(
        f'📍 Кабинет №{kabinet.class_num}\n'
        f'🧭 Как пройти: {kabinet.description}'
    )

