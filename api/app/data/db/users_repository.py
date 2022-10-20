from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from typing import List, Optional

from app.data.models.admin_users import AdminUser
from app.data.models.subscription import SubscriptionUser
from app.data.models.users import User


class UsersRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = select(User).options(joinedload(User.subscription)).filter(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_all_users(self) -> List[User]:
        stmt = select(User).options(selectinload(User.subscription).options(
            joinedload(SubscriptionUser.subscription)
        ))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_all_users_with_active_subscriptions(self) -> List[User]:
        stmt = select(User).options(joinedload(User.subscription.and_(SubscriptionUser.active == True), innerjoin=True)).filter(User.telegram_user_id != None)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create_user(self, name: str, phone: str) -> User:
        user = User(
            name=name,
            phone=phone
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        await self._session.commit()

        return user

    async def update_user(
            self,
            user_id: int,
            name: str,
            phone: str,
    ) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return None

        user.name = name
        user.phone = phone

        await self._session.commit()

        return user
