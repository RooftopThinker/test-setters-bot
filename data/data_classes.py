import sqlalchemy
from datetime import datetime, timedelta
from .database import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=False)
    telegram_username = sqlalchemy.Column(sqlalchemy.String)
    telegram_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    last_button_chosen = sqlalchemy.Column(sqlalchemy.String)

class ButtonClickLog(SqlAlchemyBase):
    __tablename__ = 'button_click_logs'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('users.telegram_id'), nullable=False)
    button_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    clicked_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)