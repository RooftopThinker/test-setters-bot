from data import User
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy


async def get_user(telegram_id: int, session: AsyncSession) -> User:
    request = sqlalchemy.select(User).filter(User.telegram_id == telegram_id)
    user: User = await session.scalar(request)
    return user


