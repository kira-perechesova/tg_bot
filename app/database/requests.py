from sqlalchemy import select

from app.database.models import async_session
from app.database.models import User, Classes, Teacher, Kabinet


async def set_user(tg_id: int) -> None: # none?
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_classes():
    async with async_session() as session:
        result = await session.scalars(select(Classes))
        return result.all()

async def get_class_teacher(class_nl: str):
    async with async_session() as session:
        stmt = select(Classes).where(Classes.class_nl == class_nl)
        class_obj = await session.scalar(stmt)
        if class_obj:
            teacher = await session.get(Teacher, class_obj.teacher)
            return teacher
        return None

async def get_teacher_classes(teacher_id: int):
    async with async_session() as session:
        stmt = select(Classes).where(Classes.teacher == teacher_id)
        result = await session.scalars(stmt)
        return result.all()


async def get_kabinet_by_number(class_num: int):
    async with async_session() as session:
        stmt = select(Kabinet).where(Kabinet.class_num == class_num)
        return await session.scalar(stmt)
