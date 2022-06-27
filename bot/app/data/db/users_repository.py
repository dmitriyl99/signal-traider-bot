from sqlalchemy.orm import Session

from . import async_session
from sqlalchemy.future import select
from app.data.models.users import User


async def get_user_by_telegram_id(telegram_user_id: int) -> User:
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_user_id == telegram_user_id))
        return result.scalars().first()


async def save_user(name: str, phone: str, telegram_user_id: int) -> User:
    user = User(
        name=name,
        phone=phone,
        telegram_user_id=telegram_user_id
    )
    async with async_session() as session:
        session.add(user)
        await session.commit()

    return user
