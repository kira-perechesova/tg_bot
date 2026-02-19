from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from datetime import datetime

import app.keyboards as kb
import app.database.requests as rq

router = Router()


# Определяем состояния для FSM
class Form(StatesGroup):
    waiting_for_class_teacher = State()  # Ждем класс для поиска классного руководителя
    waiting_for_class_schedule = State()  # Ждем класс для расписания класса
    waiting_for_kabinet = State()  # Ждем номер кабинета
    waiting_for_teacher_schedule = State()  # Ждем ФИО учителя для расписания


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        'Здравствуйте!\nЯ бот, созданный президентом гимназии №24 Перечесовой Кирой в 2026 году.',
        reply_markup=kb.main
    )


@router.message(F.text == 'Классные руководители')
async def class_teacher_start(message: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_class_teacher)
    await message.answer(
        'Введите номер класса (например: 10Б):'
    )


@router.message(Form.waiting_for_class_teacher, F.text.regexp(r'^\d{1,2}[А-ЯA-Z]$'))
async def show_class_teacher(message: Message, state: FSMContext):
    class_nl = message.text.upper()

    teacher = await rq.get_class_teacher(class_nl)

    if not teacher:
        await message.answer(
            f'❌ Класс {class_nl} не найден или классный руководитель не указан'
        )
        await state.clear()
        return

    await message.answer(
        f'👩‍🏫 Классный руководитель {class_nl}:\n'
        f'{teacher.name}'
    )
    await state.clear()


@router.message(Form.waiting_for_class_teacher)
async def invalid_class_format_for_teacher(message: Message, state: FSMContext):
    await message.answer(
        'Неверный формат класса. Пожалуйста, введите номер класса в формате "10Б":'
    )


@router.message(F.text == 'Замены')
async def send_zameny(message: Message):
    file = FSInputFile('app/files/замены_на_21.01.2026.jpg')
    await message.answer_document(
        document=file,
        caption='Актуальные замены'
    )


@router.message(F.text == 'Кабинеты')
async def kabinet_start(message: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_kabinet)
    await message.answer(
        'Введите номер кабинета (например: 51):'
    )


@router.message(Form.waiting_for_kabinet, F.text.regexp(r'^\d+$'))
async def kabinet_search(message: Message, state: FSMContext):
    kabinet_number = int(message.text)

    kabinet = await rq.get_kabinet_by_number(kabinet_number)

    if not kabinet:
        await message.answer(
            f'Кабинет №{kabinet_number} не найден в базе данных'
        )
        await state.clear()
        return

    await message.answer(
        f'📍 Кабинет №{kabinet.class_num}\n'
        f'🧭 Как пройти: {kabinet.description}'
    )
    await state.clear()


@router.message(Form.waiting_for_kabinet)
async def invalid_kabinet_format(message: Message, state: FSMContext):
    await message.answer(
        'Неверный формат номера кабинета. Пожалуйста, введите только цифры (например: 51):'
    )


@router.message(F.text == 'Расписание класса')
async def schedule_start(message: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_class_schedule)
    await message.answer(
        'Введите номер класса (например: 10Б):'
    )


@router.message(Form.waiting_for_class_schedule, F.text.regexp(r'^\d{1,2}[А-ЯA-Z]$'))
async def send_student_schedule(message: Message, state: FSMContext):
    class_n = message.text.upper()

    schedule = await rq.get_student_schedule(class_n)

    if not schedule:
        await message.answer(
            f'Расписание для класса {class_n} не найдено'
        )
        await state.clear()
        return

    file = FSInputFile(schedule.path_r)

    await message.answer_document(
        document=file,
        caption=f'Расписание для {class_n}'
    )
    await state.clear()


@router.message(Form.waiting_for_class_schedule)
async def invalid_class_format_for_schedule(message: Message, state: FSMContext):
    await message.answer(
        'Неверный формат класса. Пожалуйста, введите номер класса в формате "10Б":'
    )


@router.message(F.text == 'Расписание учителя')
async def teacher_schedule_start(message: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_teacher_schedule)
    await message.answer(
        'Введите ФИО учителя полностью (например: Загибалова Римма Ямиловна):'
    )


@router.message(Form.waiting_for_teacher_schedule, F.text)
async def send_teacher_schedule(message: Message, state: FSMContext):
    teacher_name = message.text.strip()

    schedule = await rq.get_teacher_schedule_by_name(teacher_name)

    if not schedule:
        await message.answer(
            f'Учитель "{teacher_name}" не найден или расписание отсутствует'
        )
        await state.clear()
        return

    file = FSInputFile(schedule.path_schedule)

    await message.answer_document(
        document=file,
        caption=f'Расписание учителя:\n{teacher_name}'
    )
    await state.clear()


@router.message(F.text.regexp(r'^\d{1,2}[А-ЯA-Z]$'))
async def handle_class_without_context(message: Message):
    # Обработка случая, когда пользователь ввел номер класса без выбора команды
    await message.answer(
        'Вы ввели номер класса. Пожалуйста, выберите, что вы хотите получить:\n\n'
        '1. "Классные руководители" - для поиска классного руководителя\n'
        '2. "Расписание класса" - для получения расписания класса'
    )


@router.message(F.text == 'Время урока/перемены')
async def show_current_lesson_time(message: Message):
    now = datetime.now()
    current_time = now.time()

    times = await rq.get_lesson_times()

    if not times:
        await message.answer(
            f'Текущее время: {now.strftime("%H:%M")}\n'
            f'❌ Расписание уроков не найдено'
        )
        return

    for item in times:
        try:
            start_str, end_str = item.time.split('-')

            start_time = datetime.strptime(start_str, '%H:%M').time()
            end_time = datetime.strptime(end_str, '%H:%M').time()

            if start_time <= current_time <= end_time:
                await message.answer(
                    f'Текущее время: {now.strftime("%H:%M")}\n'
                    f'📘 Сейчас {item.lesson_break}\n'
                    f'Закончится в {end_str}'
                )
                return

        except (ValueError, AttributeError) as e:
            # Пропускаем некорректные записи
            print(f"Ошибка обработки времени: {e} для записи {item}")
            continue

    # Проверяем, между какими уроками/переменами сейчас
    for i in range(len(times) - 1):
        try:
            current_end_str = times[i].time.split('-')[1]
            next_start_str = times[i + 1].time.split('-')[0]

            end_time = datetime.strptime(current_end_str, '%H:%M').time()
            next_start_time = datetime.strptime(next_start_str, '%H:%M').time()

            if end_time < current_time < next_start_time:
                await message.answer(
                    f'Текущее время: {now.strftime("%H:%M")}\n'
                    f'🕒 Сейчас перемена между уроками\n'
                    f'Следующий урок начнется в {next_start_str}'
                )
                return

        except (ValueError, IndexError, AttributeError):
            continue

    # Проверяем, до начала первого урока
    try:
        first_start_str = times[0].time.split('-')[0]
        first_start_time = datetime.strptime(first_start_str, '%H:%M').time()

        if current_time < first_start_time:
            await message.answer(
                f'Текущее время: {now.strftime("%H:%M")}\n'
                f'⏰ Уроки еще не начались\n'
                f'Первый урок начнется в {first_start_str}'
            )
            return
    except (ValueError, IndexError, AttributeError):
        pass

    # Проверяем, после окончания последнего урока
    try:
        last_end_str = times[-1].time.split('-')[1]
        last_end_time = datetime.strptime(last_end_str, '%H:%M').time()

        if current_time > last_end_time:
            await message.answer(
                f'Текущее время: {now.strftime("%H:%M")}\n'
                f'🎒 Уроки уже закончились\n'
                f'Последний урок закончился в {last_end_str}'
            )
            return
    except (ValueError, IndexError, AttributeError):
        pass

    await message.answer(
        f'Текущее время: {now.strftime("%H:%M")}\n'
        f'❌ Уроков нет'
    )