from typing import List
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from . import async_session
from app.data.models.subscription import Subscription, SubscriptionUser, SubscriptionCondition
from app.data.models.users import User

import logging

logger = logging.getLogger(__name__)


async def get_subscriptions() -> List[Subscription]:
    async with async_session() as session:
        result = await session.execute(select(Subscription))
        return result.scalars().all()


async def get_active_subscription_for_user(user: User) -> SubscriptionUser:
    async with async_session() as session:
        result = await session.execute(select(SubscriptionUser).options(joinedload(SubscriptionUser.subscription_condition)).filter(
            and_(SubscriptionUser.user_id == user.id, SubscriptionUser.active == True)
        ))
        subscription_user = result.scalars().first()
        return subscription_user


async def get_subscription_condition(subscription_id: int) -> List[SubscriptionCondition]:
    async with async_session() as session:
        result = await session.execute(
            select(SubscriptionCondition).filter(SubscriptionCondition.subscription_id == subscription_id))
        return result.scalars().all()


async def add_subscription_to_user(subscription_id: int, subscription_condition_id: int, user_id: int) -> None:
    async with async_session() as session:
        user: User = (await session.execute(select(User).filter(User.telegram_user_id == user_id))).scalars().first()
        subscription_condition = await session.get(SubscriptionCondition, subscription_condition_id)
        current_subscription_user_stmt = select(SubscriptionUser).filter(SubscriptionUser.user_id == user.id)
        result = await session.execute(current_subscription_user_stmt)
        subscription_user: SubscriptionUser = result.scalars().first()
        logger.info('Current user subscription: {}'.format(subscription_user))
        if subscription_user is None:
            subscription_user = SubscriptionUser()
            session.add(subscription_user)
        subscription_user.subscription_id = subscription_id
        subscription_user.user_id = user.id
        subscription_user.subscription_condition_id = subscription_condition_id
        subscription_user.created_at = datetime.now()
        subscription_user.active = True
        await session.commit()


async def get_subscription_by_id(subscription_id: int) -> Subscription:
    async with async_session() as session:
        return await session.get(Subscription, subscription_id)
