import asyncio

from aiogram import Dispatcher

from app.models.database import init_db
from app.config import bot

from app.handlers.start_handlers import router as start
from app.handlers.generation_handlers import router as generation


dispatcher = Dispatcher()


async def main():
    dispatcher.include_routers(start, generation)
    await init_db()
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutting down...')
    except Exception as ex:
        print(f'An error has occurred.\n{ex}')