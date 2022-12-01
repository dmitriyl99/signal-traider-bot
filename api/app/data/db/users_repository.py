import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from sqlalchemy import update, or_
from typing import List, Optional

from app.data.models.admin_users import AdminUser
from app.data.db import Session
from app.data.models.subscription import SubscriptionUser
from app.data.models.users import User
from app.helpers import array

from app.helpers import paginator


class UsersRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = select(User).options(joinedload(User.subscription)).filter(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_all_users(self, analyst_id: int = None, page: int = 1, per_page: int = 25, search: str| None = None) -> paginator.Paginator:
        with Session() as session:
            query = session.query(User).options(selectinload(User.subscription).options(
                joinedload(SubscriptionUser.subscription)
            ))
            if analyst_id:
                query = query.filter(User.analyst_id == analyst_id)
            if search and search != '':
                query = query.filter(or_(User.name.like(f"%{search}%"), User.phone.like(f"%{search}%")))
            return paginator.paginate(query, page, per_page)

    async def get_all_users_with_active_subscriptions(self, analyst_id: int = None) -> List[User]:
        stmt = select(User).options(
            joinedload(User.subscription.and_(SubscriptionUser.active == True), innerjoin=True)).filter(
            User.telegram_user_id != None)
        if analyst_id is not None:
            stmt = stmt.filter(User.analyst_id == analyst_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    def divide_users_between_analytics(self):
        with Session() as session:
            admin_users: List[AdminUser] = session.query(AdminUser).options(
                subqueryload(AdminUser.roles)
            ).all()
            analysts_users = []
            for admin_user in admin_users:
                if len(list(filter(lambda x: x.name == 'Analyst', admin_user.roles))) > 0:
                    analysts_users.append(admin_user)
            session.execute(update(User).where(User.analyst_id != None).values(analyst_id=None))
            all_users = session.query(User).all()
            chunk_size = round(len(all_users) / len(analysts_users)) + 1
            chunked_users = array.chunks(all_users, chunk_size)
            for idx, users in enumerate(chunked_users):
                for user in users:
                    user.analyst_id = analysts_users[idx].id
            session.commit()

    async def create_user(self, name: str, phone: str) -> User:
        stmt = select(User).filter(User.phone == phone)
        result = await self._session.execute(stmt)
        user = result.scalars().first()
        if user:
            return user
        user = User(
            name=name,
            phone=phone,
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
