from sqlalchemy.orm import Session

from . import engine
from app.data.models.users import User


def get_user_by_telegram_id(telegram_user_id: int) -> User:
    with Session(engine) as session:
        return session.query(User).filter(User.telegram_user_id == telegram_user_id).first()


def save_user(name: str, phone: str, telegram_user_id: int) -> User:
    user = User(
        name=name,
        phone=phone,
        telegram_user_id=telegram_user_id
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()

    return user
