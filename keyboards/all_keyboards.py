from aiogram import types

def get_interest_keyboard():
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Искусственный интеллект", callback_data="topic:Искусственный интеллект"),
            types.InlineKeyboardButton(text="Маркетинг", callback_data="topic:Маркетинг"),
        ],
        [
            types.InlineKeyboardButton(text="Дизайн", callback_data="topic:Дизайн"),
            types.InlineKeyboardButton(text="Аналитика", callback_data="topic:Аналитика"),
        ]
    ])
    return keyboard


def cancel():
    buttons = [[types.InlineKeyboardButton(text="Отмена", callback_data='cancel')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def admin_menu():
    buttons = [[types.InlineKeyboardButton(text='Статистика', callback_data='stats')],
               [types.InlineKeyboardButton(text='Рассылка', callback_data='mailing')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def yes_or_no():
    buttons = [[types.InlineKeyboardButton(text='Да✅', callback_data='yes')],
               [types.InlineKeyboardButton(text='Нет❌', callback_data='no')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def mailing_options():
    buttons = [
        [types.InlineKeyboardButton(text='Всем пользователям', callback_data='mailing_all')],
        [types.InlineKeyboardButton(text='Пользователям выбравшим ИИ', callback_data='Искусственный интеллект')],
        [types.InlineKeyboardButton(text='Пользователям выбравшим Дизайн', callback_data='Дизайн')],
        [types.InlineKeyboardButton(text='Пользователям выбравшим Аналитику', callback_data='Аналитика')],
        [types.InlineKeyboardButton(text='Пользователям выбравшим Маркетинг', callback_data='Маркетинг')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


