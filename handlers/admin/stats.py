from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession
from filters.is_a_member_of_admin_chat import IsAdmin
from data import User, ButtonClickLog
import sqlalchemy
router = Router()
router.message.filter(IsAdmin())

@router.callback_query(F.data == 'stats')
async def stats(callback: types.CallbackQuery, session: AsyncSession):
    # Количество пользователей
    total_users = await session.scalar(sqlalchemy.select(sqlalchemy.func.count()).select_from(User))

    # Переходы по кнопкам
    AI_clicks = await session.scalar(sqlalchemy.select(sqlalchemy.func.count()).select_from(ButtonClickLog).where(ButtonClickLog.button_name == "Искусственный интеллект"))
    analytics_clicks = await session.scalar(sqlalchemy.select(sqlalchemy.func.count()).select_from(ButtonClickLog).where(ButtonClickLog.button_name == "Аналитика"))
    design_clicks = await session.scalar(sqlalchemy.select(sqlalchemy.func.count()).select_from(ButtonClickLog).where(ButtonClickLog.button_name == "Дизайн"))
    marketing_clicks = await session.scalar(sqlalchemy.select(sqlalchemy.func.count()).select_from(ButtonClickLog).where(ButtonClickLog.button_name == "Маркетинг"))

    text = (
        'Статистика по боту:\n'
        f'- Количество пользователей: <b>{total_users}</b>\n'
        
        'Переходы по кнопкам:\n'
        f'- Искусственный интеллект: <b>{AI_clicks}</b>\n'
        f'- Аналитика: <b>{analytics_clicks}</b>\n'
        f'- Дизайн: <b>{design_clicks}</b>\n'
        f'- Маркетинг: <b>{marketing_clicks}</b>'
    )
    await callback.message.answer(text, parse_mode='HTML')
    await callback.answer()

