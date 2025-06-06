import sqlalchemy
from aiogram import Router, F, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from data import User
from filters import IsAdmin
from keyboards.all_keyboards import cancel, yes_or_no, mailing_options
from aiogram.fsm.context import FSMContext
from ..fsm import SendMailing
from typing import List
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from asyncio import sleep
router = Router()
router.message.filter(IsAdmin())


@router.callback_query(F.data == 'mailing')
async def show_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Выберите тип рассылки:', reply_markup=mailing_options())


@router.callback_query(F.data.in_({'mailing_all', 'Искусственный интеллект', 'Дизайн', 'Аналитика', 'Маркетинг'}))
async def set_mailing_type(callback: types.CallbackQuery, state: FSMContext):
    mailing_type = callback.data
    await state.update_data(mailing_type=mailing_type)
    await callback.message.answer(text='Пришлите сообщение, которое необходимо отправить пользователям',
                         reply_markup=cancel())
    await state.set_state(SendMailing.approve)


@router.message(SendMailing.approve, ~F.media_group_id)
async def approve(message: types.Message, state: FSMContext):
    await state.update_data(message_id=message.message_id, chat_id=message.chat.id)
    await message.answer('Отправить рассылку?', reply_markup=yes_or_no())
    await state.set_state(SendMailing.send_mailing)


@router.callback_query(SendMailing.send_mailing, F.data == 'yes')
async def send_mailing(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.edit_text('Рассылка запущена..', reply_markup=None)
    data = await state.get_data()
    
    # Build query based on mailing type
    query = sqlalchemy.select(User)
    if data.get('mailing_type', 'mailing_all') != 'mailing_all':
        query = query.filter(User.last_button_chosen == data.get('mailing_type'))

    result: List[User] = list(await session.scalars(query))
    bot_blocked_info = ''
    bot_blocked_counter = 0
    await state.clear()
    
    for user in result:
        try:
            await callback.bot.copy_message(from_chat_id=data['chat_id'], message_id=data['message_id'],
                                            chat_id=user.telegram_id)
            await sleep(0.05)
        except TelegramForbiddenError:
            bot_blocked_counter+=1
            bot_blocked_info+=f"Username: {user.telegram_username}\n"
            f"Отображаемое имя: {user.telegram_name}\n"

    if bot_blocked_counter:
        try:
            await callback.message.answer(f'Рассылка завершена.'
                                f' Сообщение не было доставлено пользователям, заблокировавшим бота:\n {bot_blocked_info}')
        except TelegramBadRequest:
            await callback.message.answer(f"Рассылка завершена. "
                                 f"Сообщение не было доставлено пользователям, заблокировавшим бота{bot_blocked_counter}")
    else:
        await callback.message.answer(f"Рассылка завершена. ")


@router.callback_query(SendMailing.send_mailing, F.data == 'no')
async def send_mailing(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()