from typing import Tuple
from datetime import date
from dateutil import relativedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from app.data.models.users import User
from app.data.models.subscription import SubscriptionUser


class StatisticsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def users_statistics(self) -> Tuple[int, int, int]:
        today = date.today()
        yesterday = today - relativedelta.relativedelta(days=1)

        all_users_count_stmt = select(func.count(User.id))
        all_users_count_result = await self._session.execute(all_users_count_stmt)
        all_users_count = all_users_count_result.scalars().one()

        new_users_count_stmt = select(func.count(User.id)).filter(func.date(User.created_at) == today)
        new_users_count_result = await self._session.execute(new_users_count_stmt)
        new_users_count = new_users_count_result.scalars().one()

        yesterday_users_count_stmt = select(func.count(User.id)).filter(func.date(User.created_at) == yesterday)
        yesterday_users_count_result = await self._session.execute(yesterday_users_count_stmt)
        yesterday_users_count = yesterday_users_count_result.scalars().one()
        users_growth_count = new_users_count - yesterday_users_count

        return all_users_count, new_users_count, users_growth_count

    async def get_subscription_statistics(self) -> Tuple[int, int, int, int]:
        today = date.today()
        yesterday = today - relativedelta.relativedelta(days=1)

        all_active_subscriptions_stmt = select(func.count(SubscriptionUser.user_id)).filter(SubscriptionUser.active == True)
        all_active_subscriptions_count = await self._get_result(all_active_subscriptions_stmt)

        new_subscriptions_count_stmt = select(func.count(SubscriptionUser.user_id)).filter(func.date(SubscriptionUser.created_at) == today)
        new_subscriptions_count = await self._get_result(new_subscriptions_count_stmt)

        yesterday_subscriptions_count_stmt = select(func.count(SubscriptionUser.user_id)).filter(func.date(SubscriptionUser.created_at) == yesterday)
        yesterday_subscriptions_count = await self._get_result(yesterday_subscriptions_count_stmt)
        subscriptions_growth_count = new_subscriptions_count - yesterday_subscriptions_count

        users_without_subscriptions_stmt = select(User).options(selectinload(User.subscription)).filter(~User.subscription.has())
        users_without_subscriptions_result = await self._session.execute(users_without_subscriptions_stmt)
        users_without_subscriptions = users_without_subscriptions_result.scalars().all()
        users_without_subscriptions_count = len(users_without_subscriptions)

        return all_active_subscriptions_count, new_subscriptions_count, subscriptions_growth_count, users_without_subscriptions_count

    async def _get_result(self, stmt) -> int:
        result = await self._session.execute(stmt)
        return result.scalars().one()


