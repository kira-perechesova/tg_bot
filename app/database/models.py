from sqlalchemy import BigInteger, String, ForeignKey
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

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)






