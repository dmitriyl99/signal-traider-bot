from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, filters

from app.payments import providers as payment_providers, handlers
from app.data.db import subscriptions_repository
from app.helpers import array
from app.resources import strings

from app.services import currency_exchange as currency_exchange_service
from app.actions import send_subscriptions, send_subscription_conditions, send_payment_providers


CHOOSE_SUBSCRIPTION, CHOOSE_CONDITION, SELECT_PAYMENT_PROVIDER, BACK = range(4)


async def _start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await send_subscriptions(update)

    return CHOOSE_SUBSCRIPTION


async def _choose_subscription(update: Update, context: CallbackContext.DEFAULT_TYPE):
    subscription = await subscriptions_repository.get_subscription_by_name(update.message.text)
    if subscription is None:
        await update.message.reply_text("Такая подписка не найдена")
        return CHOOSE_SUBSCRIPTION
    subscription_id = subscription.id
    context.user_data['subscription:id'] = subscription_id
    await send_subscription_conditions(update, subscription_id)
    return CHOOSE_CONDITION


async def _choose_condition(update: Update, context: CallbackContext.DEFAULT_TYPE):
    async def error():
        await update.message.reply_text('Выбрано не праивльное условие подписки')
        return CHOOSE_CONDITION
    message = update.message
    # In this action need to send payment invoice, but for now without
    message_data = message.text
    if 'Назад' in message_data:
        await send_subscriptions(update)
        return CHOOSE_SUBSCRIPTION
    if 'месяц' not in message_data:
        return await error()
    splitted_message_data = message_data.split(' ')
    if len(splitted_message_data) <= 1:
        return await error()
    subscription_id = context.user_data['subscription:id']
    subscription_condition_duration_in_month = int(splitted_message_data[0])
    subscription_condition = await subscriptions_repository.find_condition_by_subscription_id_and_duration(subscription_id, subscription_condition_duration_in_month)
    if subscription_condition is None:
        return await error()
    subscription_condition_id = subscription_condition.id
    context.user_data['subscription:condition_id'] = subscription_condition_id

    await send_payment_providers(update, context, subscription_id, subscription_condition_id)

    return SELECT_PAYMENT_PROVIDER


async def _select_payment_provider(update: Update, context: CallbackContext.DEFAULT_TYPE):
    message = update.message
    subscription_id = context.user_data['subscription:id']
    subscription_condition_id = context.user_data['subscription:condition_id']
    if message.text == 'Назад':
        await send_subscription_conditions(update, subscription_id)
        return CHOOSE_CONDITION
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    payment_provider_name = message.text
    payment_provider = payment_providers.get_payment_provider_by_name(payment_provider_name)
    exchanged_price = currency_exchange_service.convert_usd_to_uzs(subscription_condition.price / 100)
    if payment_provider is None:
        await update.message.reply_text('Выбран провайдер, которого мы не поддерживаем')
        return SELECT_PAYMENT_PROVIDER
    message = await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title='Оплатить подписку',
        description='%s на %d месяцев за $%d' % (
            subscription.name,
            subscription_condition.duration_in_month,
            subscription_condition.price / 100
        ),
        payload='subscription:%d:%d:%d:%s' % (update.effective_user.id, subscription_id, subscription_condition_id, payment_provider_name),
        provider_token=payment_provider.provider_token,
        currency='UZS',
        prices=[
            LabeledPrice('%d месяцев' % subscription_condition.duration_in_month, int(exchanged_price) * 100)
        ],
    )
    context.user_data['invoice_message_id'] = message.message_id
    back_message = await context.bot.send_message(update.effective_chat.id, 'Для отмены нажмите кнопку "Назад"', reply_markup=ReplyKeyboardMarkup([['Назад']], resize_keyboard=True))
    context.user_data['back_message_id'] = back_message.message_id

    return BACK


async def _back_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    subscription_id = context.user_data['subscription:id']
    subscription_condition_id = context.user_data['subscription:condition_id']
    await send_payment_providers(update, context, subscription_id, subscription_condition_id)

    return SELECT_PAYMENT_PROVIDER


async def _fallbacks_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.pre_checkout_query:
        await handlers._pre_checkout_subscription(update, context)
    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(strings.choose_subscription_text), _start)],
    states={
        CHOOSE_SUBSCRIPTION: [MessageHandler(filters.TEXT, _choose_subscription)],
        CHOOSE_CONDITION: [MessageHandler(filters.TEXT, _choose_condition)],
        SELECT_PAYMENT_PROVIDER: [MessageHandler(filters.TEXT, _select_payment_provider)],
        BACK: [MessageHandler(filters.TEXT, _back_handler)]
    },
    fallbacks=[MessageHandler(filters.TEXT, _fallbacks_handler)]
)

