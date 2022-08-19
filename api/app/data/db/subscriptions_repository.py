from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models.subscription import Subscription, SubscriptionUser
from app.data.models.users import User


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
            subscription_condition_id: int,
            proactively_added=True
    ) -> SubscriptionUser:
        subscription_user = SubscriptionUser()
        subscription_user.subscription_id = subscription_id
        subscription_user.subscription_condition_id = subscription_condition_id
        subscription_user.proactively_added = proactively_added
        subscription_user.user_id = user.id
        self._session.add(subscription_user)
        await self._session.commit()

        return subscription_user
