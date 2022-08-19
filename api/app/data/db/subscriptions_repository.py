from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models.subscription import Subscription, SubscriptionCondition


class SubscriptionsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_subscriptions_list(self) -> List[Subscription]:
        stmt = select(Subscription).options(selectinload(Subscription.conditions))
        result = await self._session.execute(stmt)
        return result.scalars().all()
