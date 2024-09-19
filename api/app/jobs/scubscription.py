from typing import List
from datetime import datetime
import logging

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.data.db import async_session
from app.data.models.subscription import SubscriptionUser, Subscription
from app.helpers import date
from app.services import bot
from app.config import settings
from aiogram import Bot, types

logger = logging.getLogger(__name__)


async def check_all_subscriptions_job():
    stmt = select(SubscriptionUser).options(
        joinedload(SubscriptionUser.user),
    ).filter(SubscriptionUser.active == True).filter(SubscriptionUser.activation_datetime != None)
    logger.info('Start job to deactivate subscriptions')
    tg_bot = Bot(settings.telegram_bot_api_token)
    async with async_session() as session:
        result = await session.execute(stmt)
        active_subscriptions: List[SubscriptionUser] = result.scalars().all()
        logger.info('Active subscription found: %d' % len(active_subscriptions))
        for subscription in active_subscriptions:
            diff_in_days = date.diff_in_days(subscription.activation_datetime, datetime.now())
            if abs(diff_in_days) >= subscription.duration_in_days:
                if abs(diff_in_days) - subscription.duration_in_days in [0, 1]:
                    if subscription.notified_1_day_after is False:
                        subscription_entity: Subscription = await session.get(Subscription, subscription.subscription_id)
                        try:
                            await tg_bot.send_message(
                                chat_id=subscription.user.telegram_user_id,
                                text='Толовни давом этириш учун @shakhriyor_toshpulatov мурожат қилин',
                                parse_mode=types.ParseMode.HTML,
                            )
                        except:
                            pass
                else:
                    logger.info(
                        'Deactivate subscription %d for user %d' % (subscription.subscription_id, subscription.user_id))
                    subscription.active = False
                    await session.commit()
                    subscription_entity: Subscription = await session.get(Subscription, subscription.subscription_id)
                    telegram_group_chat_id = settings.telegram_group_id
                    try:
                        await bot.ban_user_in_group(subscription.user.telegram_user_id, telegram_group_chat_id)
                    except:
                        pass
                    # amocrm_integration.add_user_to_catalog(subscription.user, amocrm_integration.AmoCrmUserType.LOST_USER)

                    await tg_bot.send_message(
                        chat_id=subscription.user.telegram_user_id,
                        text='Толовни давом этириш учун @shakhriyor_toshpulatov мурожат қилин',
                        parse_mode=types.ParseMode.HTML,
                    )
            # elif subscription.duration_in_days - abs(diff_in_days) == 3:
            #     logger.info(f'renew_subscription:{subscription.user.telegram_user_id},{subscription.subscription_id},{subscription.user_id}')
            #     if subscription.notified_3_days is False:
            #         subscription_entity: Subscription = await session.get(Subscription, subscription.subscription_id)
            #         await tg_bot.send_message(
            #             chat_id=subscription.user.telegram_user_id,
            #             text='До оночания вашей подписки <b>{name}</b> осталось 3 дня. Продлите подписку, чтобы не потерять доступ к группе.'.format(
            #                 name=subscription_entity.name),
            #             parse_mode=types.ParseMode.HTML,
            #             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            #                 types.InlineKeyboardButton(text="Продлить", callback_data=f'renew_subscription:{subscription.user.telegram_user_id},{subscription.subscription_id},{subscription.user_id}')
            #             ]])
            #         )
            #         subscription.notified_3_days = True
            #         await session.commit()
