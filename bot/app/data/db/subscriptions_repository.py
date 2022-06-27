from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import get_session
from app.data.models.subscription import Subscription, SubscriptionUser, SubscriptionCondition
from app.data.models.users import User


async def get_subscriptions() -> List[Subscription]:
    session = get_session()
    return await session.query(Subscription).all()


async def get_active_subscription_for_user(user_id: int) -> Subscription:
    session = get_session()
    subscription_user = await session.query(SubscriptionUser).filter(
        and_(SubscriptionUser.user_id == user_id, SubscriptionUser.active is True)
    ).first()
    return subscription_user.subscription


async def get_subscription_condition(subscription_id: int) -> List[SubscriptionCondition]:
    session = get_session()
    return await session.query(SubscriptionCondition).filter(SubscriptionCondition.subscription_id == subscription_id).all()


async def add_subscription_to_user(subscription_id: int, subscription_condition_id: int, user_id: int) -> None:
    session = get_session()
    user = session.query(User).filter(User.telegram_user_id == user_id).first()
    subscription_condition = session.query(SubscriptionCondition).get(subscription_condition_id)
    user.subscriptions.append(SubscriptionUser(
        subscription_condition=subscription_condition,
        subscription_id=subscription_id,
        active=True
    ))
    await session.commit()


async def get_subscription_by_id(subscription_id: int) -> Subscription:
    session = get_session()
    return await session.query(Subscription).get(subscription_id)
