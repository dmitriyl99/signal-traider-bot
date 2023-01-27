from typing import List, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import and_, or_
from sqlalchemy.future import select

from . import async_session
from app.data.models.subscription import Subscription, SubscriptionUser, SubscriptionCondition
from app.data.models.users import User
from app.helpers import date as date_helper

import logging

logger = logging.getLogger(__name__)


async def get_subscriptions(category: str | None = None) -> List[Subscription]:
    async with async_session() as session:
        stmt = select(Subscription)
        if category:
            category = category.lower()
            stmt = stmt.filter(Subscription.category == category)
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_active_subscription_for_user(user: User) -> SubscriptionUser:
    async with async_session() as session:
        result = await session.execute(select(SubscriptionUser).filter(
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
        subscription_user: SubscriptionUser = (await session.execute(
            select(SubscriptionUser).filter(SubscriptionUser.user_id == user.id))).scalars().first()
        subscription_condition: SubscriptionCondition = await session.get(SubscriptionCondition,
                                                                          subscription_condition_id)

        if subscription_user is None:
            subscription_user = SubscriptionUser()
            session.add(subscription_user)
        subscription_user.subscription_id = subscription_id
        subscription_user.user_id = user.id

        now_datetime = datetime.now()
        subscription_end_date = now_datetime + relativedelta(
            months=subscription_condition.duration_in_month)
        subscription_user.duration_in_days = date_helper.diff_in_days(now_datetime, subscription_end_date)
        subscription_user.created_at = now_datetime
        subscription_user.active = True
        subscription_user.activation_datetime = now_datetime
        await session.commit()


async def add_subscription_with_days_to_user(
        user: User,
        subscription_id: int,
        duration_in_days: int,
) -> SubscriptionUser:
    current_subscription_user_stmt = select(SubscriptionUser).filter(SubscriptionUser.user_id == user.id)
    async with async_session() as session:
        result = await session.execute(current_subscription_user_stmt)
        subscription_user: SubscriptionUser = result.scalars().first()
        if subscription_user is None:
            subscription_user = SubscriptionUser()
        subscription_user.subscription_id = subscription_id
        subscription_user.duration_in_days = duration_in_days
        subscription_user.proactively_added = False
        subscription_user.user_id = user.id
        subscription_user.active = True
        session.add(subscription_user)
        await session.commit()

        return subscription_user


async def get_subscription_by_id(subscription_id: int) -> Subscription:
    async with async_session() as session:
        return await session.get(Subscription, subscription_id)


async def get_subscription_by_name(subscription_name: str) -> Optional[Subscription]:
    async with async_session() as session:
        stmt = select(Subscription).filter(Subscription.name == subscription_name)
        result = await session.execute(stmt)
        return result.scalars().first()


async def find_condition_by_subscription_id_and_duration(subscription_id: int, duration: int) -> Optional[SubscriptionCondition]:
    async with async_session() as session:
        stmt = select(SubscriptionCondition).filter(or_(and_(SubscriptionCondition.subscription_id == subscription_id,
                                                    SubscriptionCondition.duration_in_month == duration),
                                                        SubscriptionCondition.duration_in_days == duration))
        result = await session.execute(stmt)
        return result.scalars().first()
