from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import engine
from app.data.models.subscription import Subscription, SubscriptionUser, SubscriptionCondition
from app.data.models.users import User


def get_subscriptions() -> List[Subscription]:
    with Session(engine) as session:
        return session.query(Subscription).all()


def get_active_subscription_for_user(user_id: int) -> Subscription:
    with Session(engine) as session:
        subscription_user = session.query(SubscriptionUser).filter(
            and_(SubscriptionUser.user_id == user_id, SubscriptionUser.active is True)
        ).first()

        return subscription_user.subscription


def get_subscription_condition(subscription_id: int) -> List[SubscriptionCondition]:
    with Session(engine) as session:
        return session.query(SubscriptionCondition).filter(SubscriptionCondition.subscription_id == subscription_id).all()


def add_subscription_to_user(subscription_id: int, subscription_condition_id: int, user_id: int) -> None:
    with Session(engine) as session:
        print(user_id)
        user = session.query(User).filter(User.telegram_user_id == user_id).first()
        subscription_condition = session.query(SubscriptionCondition).get(subscription_condition_id)
        user.subscriptions.append(SubscriptionUser(
            subscription_condition=subscription_condition,
            subscription_id=subscription_id,
            active=True
        ))
        session.commit()


def get_subscription_by_id(subscription_id: int) -> Subscription:
    with Session(engine) as session:
        return session.query(Subscription).get(subscription_id)
