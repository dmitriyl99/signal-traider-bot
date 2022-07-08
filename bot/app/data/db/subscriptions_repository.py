from typing import List

from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from . import async_session
from app.data.models.subscription import Subscription, SubscriptionUser, SubscriptionCondition
from app.data.models.users import User


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
        user = (await session.execute(select(User).filter(User.telegram_user_id == user_id))).scalars().first()
        subscription_condition = await session.get(SubscriptionCondition, subscription_condition_id)
        current_subscription_user_stmt = select(SubscriptionUser).filter(SubscriptionUser.user_id == user_id)
        current_subscription_user = (await session.execute(current_subscription_user_stmt)).scalars().first()
        if current_subscription_user is not None:
            current_subscription_user.delete()
            await session.commit()
        subscription_user = SubscriptionUser(
            subscription_condition=subscription_condition,
            subscription_id=subscription_id,
            active=True,
            user_id=user.id
        )
        session.add(subscription_user)
        await session.commit()


async def get_subscription_by_id(subscription_id: int) -> Subscription:
    async with async_session() as session:
        return await session.get(Subscription, subscription_id)
