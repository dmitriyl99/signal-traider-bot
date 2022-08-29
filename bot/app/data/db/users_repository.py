from datetime import datetime

from . import async_session
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.data.models.users import User
from app.data.models.subscription import SubscriptionUser


async def get_user_by_telegram_id(telegram_user_id: int) -> User:
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_user_id == telegram_user_id))
        return result.scalars().first()


async def save_user(name: str, phone: str, telegram_user_id: int) -> User:
    stmt = select(User).filter(User.phone == phone)
    async with async_session() as session:
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user is None:
            user = User(
                name=name,
                phone=phone,
            )
            session.add(user)
        user.telegram_user_id = telegram_user_id
        user.registration_date = datetime.now()
        await session.commit()

    return user


async def check_for_proactively_added_user(phone: str, telegram_user_id: int) -> bool:
    stmt = select(User).options(joinedload(User.subscriptions.and_(SubscriptionUser.proactively_added == True))).filter(User.phone == phone)
    async with async_session() as session:
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user is None:
            return False
        if user.telegram_user_id is None:
            user.telegram_user_id = telegram_user_id
            user.registration_date = datetime.now()
        if len(user.subscriptions) > 0:
            proactively_subscription: SubscriptionUser = user.subscriptions[0]
            proactively_subscription.proactively_added = False
            proactively_subscription.active = True
            proactively_subscription.activation_datetime = datetime.now()
            await session.commit()
            return True
        await session.commit()
        return False
