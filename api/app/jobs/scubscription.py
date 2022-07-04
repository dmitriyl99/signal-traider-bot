from typing import List
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.data.db import async_session
from app.data.models.subscription import SubscriptionUser
from app.helpers import date
from app.services import bot


async def check_all_subscriptions_job():
    stmt = select(SubscriptionUser).options(
        joinedload(SubscriptionUser.subscription_condition),
        joinedload(SubscriptionUser.user),
        joinedload(SubscriptionUser.subscription)
    ).filter(SubscriptionUser.active == True)
    async with async_session() as session:
        result = await session.execute(stmt)
        active_subscriptions: List[SubscriptionUser] = result.scalars().all()
        for subscription in active_subscriptions:
            diff_in_month = date.diff_in_month(subscription.created_at, datetime.today())
            if diff_in_month == subscription.subscription_condition.duration_in_month:
                subscription.active = False
            bot.send_message_to_user(subscription.user, 'Ваша подписка {name} {months} мес. деактивирована. Отправьте команду /start чтобы приобрести подписку заново'.format(
                name=subscription.subscription.name,
                months=subscription.subscription_condition.duration_in_month)
            )
            await session.commit()
