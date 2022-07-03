from telegram import Update, SuccessfulPayment
from telegram.ext import CallbackContext, PreCheckoutQueryHandler, MessageHandler, filters

from app.data.db import subscriptions_repository, payments_repository, users_repository

_allowed_actions = ['subscription']


async def _pre_checkout_subscription(update: Update, context: CallbackContext.DEFAULT_TYPE):
    pre_checkout_query = update.pre_checkout_query
    try:
        action, telegram_user_id, subscription_id, subscription_condition_id, payment_provider = pre_checkout_query.invoice_payload.split(':')
    except ValueError:
        await pre_checkout_query.answer(ok=False, error_message='Invalid input')
        return
    if action not in _allowed_actions:
        await pre_checkout_query.answer(ok=False, error_message='Invalid payment action')
        return
    if int(telegram_user_id) != update.effective_user.id:
        await pre_checkout_query.answer(False, error_message='Попытка оплаты другим пользователем')
        return
    await pre_checkout_query.answer(True)


async def _checkout_subscription(update: Update, context: CallbackContext.DEFAULT_TYPE):
    successful_payment = update.message.successful_payment
    action, _, _, _, _ = successful_payment.invoice_payload.split(':')
    action_callback = _actions_map[action]
    await action_callback(update, context)


async def _action_subscribe(update: Update, context: CallbackContext.DEFAULT_TYPE):
    successful_payment = update.message.successful_payment
    action, telegram_user_id, subscription_id, subscription_condition_id, payment_provider = successful_payment.invoice_payload.split(':')
    await subscriptions_repository.add_subscription_to_user(int(subscription_id), int(subscription_condition_id), int(telegram_user_id))
    user = await users_repository.get_user_by_telegram_id(int(telegram_user_id))
    await payments_repository.save_payment(
        successful_payment.total_amount,
        payment_provider,
        user.id,
        int(subscription_id),
        int(subscription_condition_id)
    )
    if 'invoice_message_id' in context.user_data:
        await context.bot.delete_message(update.effective_chat.id, context.user_data['invoice_message_id'])
    await update.message.reply_text('Подписка куплена!')


_actions_map = {
    'subscription': _action_subscribe
}


handlers = [
    PreCheckoutQueryHandler(_pre_checkout_subscription),
    MessageHandler(filters.SUCCESSFUL_PAYMENT, _checkout_subscription)
]
