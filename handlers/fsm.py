from aiogram.fsm.state import State, StatesGroup

class SendMailing(StatesGroup):
    approve = State()
    send_mailing = State()
