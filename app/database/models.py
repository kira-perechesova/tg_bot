from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, async_session

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3') # подключение и создание бд

async_session = async_sessionmaker(engine) # подключение
# async_session = async_sessionmaker(engine, expire_on_commit=False)

# основной класс, который даёт возможность управлять всеми дочерними классами (всеми таблицами)
class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(90))

class Classes(Base):
    __tablename__ = 'classes'

    id: Mapped[int] = mapped_column(primary_key=True)
    class_nl: Mapped[str] = mapped_column(String(5))
    teacher: Mapped[int] = mapped_column(ForeignKey('teachers.id'))

class Kabinet(Base):
    __tablename__ = 'kabinets'

    id: Mapped[int] = mapped_column(primary_key=True)
    class_num: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(100))

class StudentSchedule(Base):
    __tablename__ = 'student_schedules'

    id: Mapped[int] = mapped_column(primary_key=True)
    class_n: Mapped[str] = mapped_column(String(5))
    path_r: Mapped[str] = mapped_column(String(255))

class TeacherSchedule(Base):
    __tablename__ = 'teacher_schedules'

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    path_schedule: Mapped[str] = mapped_column(String(255))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)






