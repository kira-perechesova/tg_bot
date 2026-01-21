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
async def class_teacher_start(message: Message):
    await message.answer(
        'Введите номер класса (например: 10Б):'
    )

@router.message(F.text.regexp(r'^\d{1,2}[А-ЯA-Z]$'))
async def show_class_teacher(message: Message):
    class_nl = message.text.upper()

    teacher = await rq.get_class_teacher(class_nl)

    if not teacher:
        await message.answer(
            f'❌ Класс {class_nl} не найден или классный руководитель не указан'
        )
        return

    await message.answer(
        f'👩‍🏫 Классный руководитель {class_nl}:\n'
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


@router.message(F.text == 'Расписание класса')
async def schedule_start(message: Message):
    await message.answer(
        'Введите номер класса (например: 10Б):'
    )

@router.message(F.text.regexp(r'^\d{1,2}[А-ЯA-Z]$'))
async def send_student_schedule(message: Message):
    class_n = message.text.upper()

    schedule = await rq.get_student_schedule(class_n)

    if not schedule:
        await message.answer(
            f'Расписание для класса {class_n} не найдено'
        )
        return

    file = FSInputFile(schedule.path_r)

    await message.answer_document(
        document=file,
        caption=f'Расписание для {class_n}'
    )


@router.message(F.text == 'Расписание учителя')
async def teacher_schedule_start(message: Message):
    await message.answer(
        'Введите ФИО учителя полностью (например: Загибалова Римма Ямиловна):'
    )

@router.message(F.text)
async def send_teacher_schedule(message: Message):
    teacher_name = message.text.strip()

    schedule = await rq.get_teacher_schedule_by_name(teacher_name)

    if not schedule:
        await message.answer(
            f'Учитель "{teacher_name}" не найден или расписание отсутствует'
        )
        return

    file = FSInputFile(schedule.path_schedule)

    await message.answer_document(
        document=file,
        caption=f'Расписание учителя:\n{teacher_name}'
    )
