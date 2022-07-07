from typing import List
from datetime import datetime
import logging

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.data.db import async_session
from app.data.models.subscription import SubscriptionUser, Subscription
from app.helpers import date
from app.services import bot

logger = logging.getLogger(__name__)


async def check_all_subscriptions_job():
    stmt = select(SubscriptionUser).options(
        joinedload(SubscriptionUser.subscription_condition),
        joinedload(SubscriptionUser.user),
    ).filter(SubscriptionUser.active == True)
    logger.info('Start job to deactivate subscriptions')
    async with async_session() as session:
        result = await session.execute(stmt)
        active_subscriptions: List[SubscriptionUser] = result.scalars().all()
        logger.info('Active subscription found: %d' % len(active_subscriptions))
        for subscription in active_subscriptions:
            diff_in_month = date.diff_in_month(subscription.created_at, datetime.now())
            if abs(diff_in_month) == subscription.subscription_condition.duration_in_month:
                logger.info('Deactivate subscription %d for user %d' % (subscription.subscription_id, subscription.user_id))
                subscription.active = False
                await session.commit()
                subscription_entity: Subscription = await session.get(Subscription, subscription.subscription_id)
                bot.send_message_to_user(subscription.user, 'Ваша подписка {name} {months} мес. деактивирована. Отправьте команду /start чтобы приобрести подписку заново'.format(
                    name=subscription_entity.name,
                    months=subscription.subscription_condition.duration_in_month)
                )
