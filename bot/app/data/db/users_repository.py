from sqlalchemy.orm import Session

from . import get_session
from app.data.models.users import User


async def get_user_by_telegram_id(telegram_user_id: int) -> User:
    session = get_session()
    return await session.query(User).filter(User.telegram_user_id == telegram_user_id).first()


async def save_user(name: str, phone: str, telegram_user_id: int) -> User:
    user = User(
        name=name,
        phone=phone,
        telegram_user_id=telegram_user_id
    )
    session = get_session()
    session.add(user)
    await session.commit()

    return user
