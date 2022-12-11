from typing import List, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models.subscription import Subscription, SubscriptionUser, SubscriptionCondition
from app.data.models.users import User
from app.helpers import date as date_helper


class SubscriptionsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_subscriptions_list(self) -> List[Subscription]:
        stmt = select(Subscription).options(selectinload(Subscription.conditions))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def add_subscription_to_user(
            self,
            user: User,
            subscription_id: int,
            duration_in_days: Optional[int] = None,
            subscription_condition_id: Optional[int] = None,
            proactively_added=True,
            active=False
    ) -> SubscriptionUser:
        current_subscription_user_stmt = select(SubscriptionUser).filter(SubscriptionUser.user_id == user.id)
        result = await self._session.execute(current_subscription_user_stmt)
        subscription_user: SubscriptionUser = result.scalars().first()
        if subscription_user is None:
            subscription_user = SubscriptionUser()
        subscription_user.subscription_id = subscription_id
        if subscription_condition_id is not None:
            subscription_condition: SubscriptionCondition = await self._session.get(SubscriptionCondition, subscription_condition_id)
            if subscription_condition is None:
                raise Exception(f"Subscription condition with id {subscription_condition_id} not found")
            now_datetime = datetime.now()
            subscription_end_date = now_datetime + relativedelta(
                months=subscription_condition.duration_in_month)
            duration_in_days = date_helper.diff_in_days(now_datetime, subscription_end_date)
        subscription_user.duration_in_days = duration_in_days
        subscription_user.proactively_added = proactively_added
        subscription_user.user_id = user.id
        subscription_user.active = active
        subscription_user.activation_datetime = datetime.now()
        self._session.add(subscription_user)
        await self._session.commit()

        return subscription_user

    async def delete_subscription_from_user(self, user_id):
        current_subscription_user_stmt = select(SubscriptionUser).filter(SubscriptionUser.user_id == user_id)
        result = await self._session.execute(current_subscription_user_stmt)
        subscription_user: SubscriptionUser = result.scalars().first()
        if subscription_user:
            await self._session.delete(subscription_user)
            await self._session.commit()
