from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.methods.send_chat_action import SendChatAction
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import config
from data import User, ButtonClickLog
from keyboards.all_keyboards import get_interest_keyboard
from openai import OpenAI
router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! 👋 Давай подберём тебе интересные темы.\nВыбери, что тебе ближе:",
        reply_markup=get_interest_keyboard()
    )


@router.callback_query(F.data.startswith("topic:"))
async def topic_click_handler(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    topic_name = callback.data.split("topic:")[1]
    user_id = callback.from_user.id

    query = select(User).where(User.telegram_id == user_id)
    user = await session.scalar(query)

    if not user:
        user = User(
            telegram_id=user_id,
            telegram_username=callback.from_user.username,
            telegram_name=callback.from_user.full_name,
        )
        session.add(user)
    user.last_button_chosen = topic_name
    await session.commit()
    log = ButtonClickLog(
        user_id=user.telegram_id,
        button_name=topic_name,
        clicked_at=datetime.now()
    )
    session.add(log)
    await session.commit()
    await callback.answer(f"Отличный выбор: {topic_name}")
    msg = await callback.message.answer("Сейчас ИИ сгенерирует для Вас небольшой совет по выбранной теме..")
    await bot.send_chat_action(chat_id=callback.from_user.id, action='typing')
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=config.OPENROUTER_KEY,
    )

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[
            {
                "role": "user",
                "content": f"Придумай очень маленький совет(<150 символов) на эту тему: {topic_name}. Отвечай по-русски"
            }
        ]
    )
    await msg.edit_text(text=completion.choices[0].message.content, parse_mode='Markdown')