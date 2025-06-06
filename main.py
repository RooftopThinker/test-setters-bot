import asyncio
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from setup_dispatcher import setup_dispatcher
from data.database import SqlAlchemyBase, engine
import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def create_metadata():
    async with engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)


async def main():
    # Start the bot
    await setup_dispatcher(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(create_metadata())
    asyncio.run(main())