from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, filters

from app.payments import providers as payment_providers
from app.data.db import subscriptions_repository
from app.helpers import array


CHOOSE_SUBSCRIPTION, CHOOSE_CONDITION,SELECT_PAYMENT_PROVIDER = range(3)


async def _start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    subscriptions = await subscriptions_repository.get_subscriptions()
    chunked_subscriptions = array.chunks(subscriptions, 2)
    keyboard = []
    for chunk in chunked_subscriptions:
        buttons = []
        for subscription in chunk:
            buttons.append(
                InlineKeyboardButton(subscription.name,
                                     callback_data='subscription_id:' + str(subscription.id)))
        keyboard.append(buttons)
    await query.answer()
    await query.edit_message_text('Выберите подписку', reply_markup=InlineKeyboardMarkup(keyboard))

    return CHOOSE_SUBSCRIPTION


async def _choose_subscription(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    # In this action need to send payment invoice, but for now without
    callback_data = query.data
    subscription_id = int(callback_data.split(':')[1])
    context.user_data['subscription:id'] = subscription_id
    subscription_conditions = await subscriptions_repository.get_subscription_condition(subscription_id)
    chunked_conditions = array.chunks(subscription_conditions, 2)
    keyboard = []
    for chunk in chunked_conditions:
        buttons = []
        for condition in chunk:
            buttons.append(
                InlineKeyboardButton('%s месяц' % condition.duration_in_month,
                                     callback_data='subscription_condition_id:' + str(condition.id)))
        keyboard.append(buttons)
    await query.edit_message_text('Выберите срок подписки', reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSE_CONDITION


async def _choose_condition(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    # In this action need to send payment invoice, but for now without
    callback_data = query.data
    subscription_condition_id = int(callback_data.split(':')[1])
    context.user_data['subscription:condition_id'] = subscription_condition_id
    subscription_id = context.user_data['subscription:id']
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    await query.answer()
    providers = payment_providers.get_payment_providers()
    keyboard_buttons = list(map(
        lambda provider: InlineKeyboardButton(provider.name,
                                              callback_data='subscription:payment_provider:' + provider.name),
        providers))
    await query.edit_message_text(text='<b>Подписка:</b> {}\n<b>Срок:</b> {}\n<b>Цена:</b> {}'.format(
        subscription.name,
        subscription_condition.duration_in_month,
        subscription_condition.price
    ), reply_markup=InlineKeyboardMarkup([keyboard_buttons]), parse_mode='HTML')

    return SELECT_PAYMENT_PROVIDER


async def _select_payment_provider(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    subscription_id = context.user_data['subscription:id']
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition_id = context.user_data['subscription:condition_id']
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    _, _, payment_provider_name = query.data.split(':')
    payment_provider = payment_providers.get_payment_provider_by_name(payment_provider_name)
    if payment_provider is None:
        await query.answer('Invalid payment provider', show_alert=True)
        return ConversationHandler.END
    await query.delete_message()
    message = await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title='Оплатить подписку',
        description='%s на %d месяцев за %d сум' % (
            subscription.name,
            subscription_condition.duration_in_month,
            subscription_condition.price / 100
        ),
        payload='subscription:%d:%d:%d:%s' % (update.effective_user.id, subscription_id, subscription_condition_id, payment_provider_name),
        provider_token=payment_provider.provider_token,
        currency='UZS',
        prices=[
            LabeledPrice('%d месяцев' % subscription_condition.duration_in_month, subscription_condition.price)
        ]
    )
    context.user_data['invoice_message_id'] = message.message_id

    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(_start, pattern='choose_subscription')],
    states={
        CHOOSE_SUBSCRIPTION: [CallbackQueryHandler(_choose_subscription, pattern=r'^subscription_id:\d')],
        CHOOSE_CONDITION: [CallbackQueryHandler(_choose_condition, pattern=r'^subscription_condition_id:\d')],
        SELECT_PAYMENT_PROVIDER: [CallbackQueryHandler(_select_payment_provider, pattern=r'^subscription:payment_provider:*')]
    },
    fallbacks=[MessageHandler(filters.TEXT, '')]
)

