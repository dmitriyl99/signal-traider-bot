from datetime import datetime
from typing import List

from . import async_session
from . import Session
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload, subqueryload
from app.data.models.users import User
from app.data.models.admin_users import AdminUser
from app.data.models.subscription import SubscriptionUser
from app.helpers import array


async def get_user_by_telegram_id(telegram_user_id: int) -> User:
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_user_id == telegram_user_id))
        return result.scalars().first()


async def set_user_language(telegram_user_id: int, language) -> User | None:
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_user_id == telegram_user_id))
        user = result.scalars().first()
        if not user:
            return None
        user.language = language
        await session.commit()
        await session.refresh(user)
    return user


def divide_users_between_analytics():
    with Session() as session:
        admin_users: List[AdminUser] = session.query(AdminUser).options(
            subqueryload(AdminUser.roles)
        ).all()
        analysts_users = []
        for admin_user in admin_users:
            if len(list(filter(lambda x: x.name == 'Analyst', admin_user.roles))) > 0:
                analysts_users.append(admin_user)
        if len(analysts_users) == 0:
            return
        session.execute(update(User).where(User.analyst_id != None).values(analyst_id=None))
        all_users = session.query(User).all()
        chunk_size = round(len(all_users) / len(analysts_users)) + 1
        chunked_users = array.chunks(all_users, chunk_size)
        for idx, users in enumerate(chunked_users):
            for user in users:
                user.analyst_id = analysts_users[idx].id
        session.commit()


async def save_user(name: str, phone: str, telegram_user_id: int, language: str) -> User:
    stmt = select(User).filter(User.phone == phone)
    async with async_session() as session:
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user is None:
            user = User(
                name=name,
                phone=phone.replace('+', ''),
                language=language,
            )
            session.add(user)
            user.telegram_user_id = telegram_user_id
            user.registration_date = datetime.now()
            await session.commit()
    divide_users_between_analytics()
    return user


async def find_user_by_phone(phone: str) -> User:
    stmt = select(User).filter(User.phone == phone)
    async with async_session() as session:
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user


async def activate_proactively_added_user(phone: str, telegram_user_id: int, language = None) -> bool:
    stmt = select(User).options(joinedload(User.subscriptions.and_(SubscriptionUser.proactively_added == True))).filter(
        User.phone == phone)
    async with async_session() as session:
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user is None:
            return False
        if user.telegram_user_id is None:
            user.telegram_user_id = telegram_user_id
            user.registration_date = datetime.now()
            print("Language", language)
            if language is not None:
                user.language = language
        if len(user.subscriptions) > 0:
            proactively_subscription: SubscriptionUser = user.subscriptions[0]
            proactively_subscription.proactively_added = False
            proactively_subscription.active = True
            await session.commit()
            return True
        await session.commit()
        return False


async def verify_user(user_id: int):
    async with async_session() as session:
        user = await session.get(User, user_id)
        user.verified_at = datetime.now()
        await session.commit()
