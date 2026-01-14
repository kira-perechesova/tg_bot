import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main()
    bot = Bot(token='8476338911:AAGmoxc6tBEFlzqC9BDykQW_duzF3IToEzA')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('бот выключен')
    # finally чтобы терминал продолжал работать и бот полностью завершал работу
    finally:
        import os
        os._exit(0)