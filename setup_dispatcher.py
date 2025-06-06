from handlers import start
from handlers.admin import show_menu, mailing, stats
from aiogram import Dispatcher
from middlewares.db import DbSessionMiddleware
from data.database import sessionmaker

async def setup_dispatcher(dispatcher: Dispatcher):
    dispatcher.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dispatcher.include_routers(start.router,
                               show_menu.router, mailing.router, stats.router)

