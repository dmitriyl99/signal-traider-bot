from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from passlib.context import CryptContext

from app.data.models.admin_users import AdminUser
from app.data.models.users import User
from app.data.models.subscription import SubscriptionUser, SubscriptionCondition


class UsersRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)

    def _create_password(self, plain_password) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(plain_password)

    async def authenticate_user(self, username: str, password: str) -> AdminUser | None:
        result = await self._session.execute(select(AdminUser).filter(AdminUser.username == username))
        user = result.scalars().first()
        if user is None:
            return user
        if not self._verify_password(password, user.password):
            return None
        return user

    async def create_admin_user(self, username: str, password: str) -> AdminUser:
        result = await self._session.execute(select(AdminUser).filter(AdminUser.username == username))
        user = result.scalars().first()
        if user:
            return user
        user = AdminUser(
            username=username,
            password=self._create_password(password)
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> AdminUser:
        return await self._session.get(AdminUser, user_id)

    async def get_all_users(self) -> List[User]:
        stmt = select(User).options(selectinload(User.subscription).options(
            joinedload(SubscriptionUser.subscription_condition).joinedload(SubscriptionCondition.subscription)
        ))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_all_users_with_active_subscriptions(self) -> List[User]:
        stmt = select(User).options(joinedload(User.subscription.and_(SubscriptionUser.active == True), innerjoin=True))
        result = await self._session.execute(stmt)
        return result.scalars().all()
