import logging

from telegram import Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    filters,
    MessageHandler,
    CallbackQueryHandler
)

from app.data.db import subscriptions_repository, users_repository
from app import actions
from app.conversations.select_subscription_conversation import _choose_subscription, _choose_condition, \
    _select_payment_provider, _back_handler, _fallbacks_handler, registration_handler

RENEW_SUBSCRIPTION = 'renew_subscription'
ARRANGE_SUBSCRIPTION = 'arrange_subscription'

CHOOSE_SUBSCRIPTION, CHOOSE_CONDITION, SELECT_PAYMENT_PROVIDER, BACK, CLOUD_PAYMENTS = range(5)


async def _renew_subscription(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    callback_data = query.data
    _, data = callback_data.split(':')
    telegram_user_id, subscription_id, user_id = data.split(',')
    logging.info(f'Renew subscription: {telegram_user_id}, {subscription_id}, {user_id}')
    if telegram_user_id != query.from_user.id:
        await query.answer("У вас нет доступа к чужому пользователю", show_alert=True)
        return
    subscription_user = await subscriptions_repository.get_subscription_user(int(subscription_id), int(user_id))
    if subscription_user is None:
        await query.answer("Не найдена подписка, пожалуйста, обратитесь к администратору", show_alert=True)
        return
    user = await users_repository.get_user_by_telegram_id(telegram_user_id)
    await actions.send_subscription_conditions(update, subscription_id, user)
    context.user_data['subscription:id'] = subscription_id
    return CHOOSE_CONDITION

handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[CallbackQueryHandler(callback=_renew_subscription, pattern=r'^renew_subscription')],
    states={
        CHOOSE_CONDITION: [MessageHandler(filters.TEXT, _choose_condition)],
        SELECT_PAYMENT_PROVIDER: [MessageHandler(filters.TEXT, _select_payment_provider)],
        BACK: [MessageHandler(filters.TEXT, _back_handler)]
    },
    fallbacks=[registration_handler, MessageHandler(filters.TEXT, _fallbacks_handler)]
)
