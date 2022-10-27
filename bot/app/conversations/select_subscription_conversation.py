from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, filters

from app.payments import providers as payment_providers, handlers
from app.data.db import subscriptions_repository, payments_repository, users_repository
from app.helpers import array

from app.services import currency_exchange as currency_exchange_service
from app.actions import send_subscriptions, send_subscription_conditions, send_payment_providers


CHOOSE_SUBSCRIPTION, CHOOSE_CONDITION, SELECT_PAYMENT_PROVIDER, BACK = range(4)


async def _start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await send_subscriptions(update)

    return CHOOSE_SUBSCRIPTION


async def _choose_subscription(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    # In this action need to send payment invoice, but for now without
    callback_data = query.data
    subscription_id = int(callback_data.split(':')[1])
    context.user_data['subscription:id'] = subscription_id
    await send_subscription_conditions(update, subscription_id)
    return CHOOSE_CONDITION


async def _choose_condition(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    # In this action need to send payment invoice, but for now without
    callback_data = query.data
    if callback_data == 'back':
        await send_subscriptions(update)
        return CHOOSE_SUBSCRIPTION
    subscription_condition_id = int(callback_data.split(':')[1])
    context.user_data['subscription:condition_id'] = subscription_condition_id
    subscription_id = context.user_data['subscription:id']
    exchanged_price, order_id = await send_payment_providers(update, context, subscription_id, subscription_condition_id)
    user = await users_repository.get_user_by_telegram_id(int(query.from_user.id))
    await payments_repository.save_payment(
        exchanged_price,
        'external',
        user.id,
        str(order_id),
        int(subscription_id),
        int(subscription_condition_id)
    )

    return SELECT_PAYMENT_PROVIDER


async def _select_payment_provider(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    subscription_id = context.user_data['subscription:id']
    subscription_condition_id = context.user_data['subscription:condition_id']
    if query.data == 'back':
        await send_subscription_conditions(update, subscription_id)
        return CHOOSE_CONDITION
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    _, _, payment_provider_name = query.data.split(':')
    payment_provider = payment_providers.get_payment_provider_by_name(payment_provider_name)
    exchanged_price = currency_exchange_service.convert_usd_to_uzs(subscription_condition.price / 100)
    if payment_provider is None:
        await query.answer('Invalid payment provider', show_alert=True)
        return ConversationHandler.END
    await query.delete_message()
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
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    providers = payment_providers.get_payment_providers()
    keyboard_buttons = list(map(
        lambda provider: InlineKeyboardButton(provider.name,
                                              callback_data='subscription:payment_provider:' + provider.name),
        providers))
    await update.message.reply_text(text='<b>Подписка:</b> {}\n<b>Срок:</b> {}\n<b>Цена:</b> ${}'.format(
        subscription.name,
        subscription_condition.duration_in_month,
        int(subscription_condition.price / 100)
    ), reply_markup=InlineKeyboardMarkup([keyboard_buttons, [InlineKeyboardButton('Назад', callback_data='back')]]), parse_mode='HTML')
    if 'invoice_message_id' in context.user_data:
        await context.bot.delete_message(update.effective_chat.id, context.user_data['invoice_message_id'])
    if 'back_message_id' in context.user_data:
        await context.bot.delete_message(update.effective_chat.id, context.user_data['back_message_id'])

    return SELECT_PAYMENT_PROVIDER


async def _fallbacks_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.pre_checkout_query:
        await handlers._pre_checkout_subscription(update, context)
    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(_start, pattern='choose_subscription')],
    states={
        CHOOSE_SUBSCRIPTION: [CallbackQueryHandler(_choose_subscription)],
        CHOOSE_CONDITION: [CallbackQueryHandler(_choose_condition)],
        SELECT_PAYMENT_PROVIDER: [CallbackQueryHandler(_select_payment_provider)],
        BACK: [MessageHandler(filters.TEXT, _back_handler)]
    },
    fallbacks=[MessageHandler(filters.TEXT, _fallbacks_handler)]
)

