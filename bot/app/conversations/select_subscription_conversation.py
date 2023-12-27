import logging

import json

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from app.payments import providers as payment_providers, handlers
from app.data.db import subscriptions_repository, users_repository, payments_repository
from app.data.models.payments import PaymentStatus
from app.resources import strings
from app.conversations.registration_conversation import handler as registration_handler

from app.services import currency_exchange as currency_exchange_service, cloud_payments
from app.actions import (send_subscriptions, send_subscription_conditions, send_payment_providers,
                         send_subscription_menu_button)

CHOOSE_SUBSCRIPTION, CHOOSE_CONDITION, SELECT_PAYMENT_PROVIDER, BACK, CLOUD_PAYMENTS = range(5)


async def _subscription_start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    message = update.message.text
    subscription = await subscriptions_repository.get_subscription_by_name(message)
    if subscription:
        context.user_data['subscription:id'] = subscription.id
        await send_subscription_conditions(update, subscription.id, user, context)
        return CHOOSE_CONDITION
    return ConversationHandler.END


async def _choose_subscription(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    if update.message.text == strings.get_string('back_button', user.language):
        await send_subscription_menu_button(update, context, user)
        return CHOOSE_SUBSCRIPTION
    subscription = await subscriptions_repository.get_subscription_by_name(update.message.text)
    if subscription is None:
        await update.message.reply_text(strings.get_string('subscription_not_found', user.language))
        return CHOOSE_SUBSCRIPTION
    subscription_id = subscription.id
    context.user_data['subscription:id'] = subscription_id
    await send_subscription_conditions(update, subscription_id, user, context)
    return CHOOSE_CONDITION


async def _choose_condition(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)

    async def error():
        await update.message.reply_text(strings.get_string('subscription_condition_wrong', user.language))
        return CHOOSE_CONDITION

    message = update.message
    # In this action need to send payment invoice, but for now without
    message_data = message.text
    if strings.get_string('back_button', user.language) in message_data:
        await send_subscriptions(update, context, user)
        return CHOOSE_SUBSCRIPTION
    if strings.get_string('subscription_month', user.language) not in message_data and \
            strings.get_string('subscription_days', user.language) not in message_data:
        return await error()
    splitted_message_data = message_data.split(' ')
    if len(splitted_message_data) <= 1:
        return await error()
    subscription_id = context.user_data['subscription:id']
    subscription_condition_duration_in_month = int(splitted_message_data[0])
    subscription_condition = await subscriptions_repository.find_condition_by_subscription_id_and_duration(
        subscription_id, subscription_condition_duration_in_month)
    if subscription_condition is None:
        return await error()
    subscription_condition_id = subscription_condition.id
    context.user_data['subscription:condition_id'] = subscription_condition_id

    await send_payment_providers(update, context, subscription_id, subscription_condition_id, user)

    return SELECT_PAYMENT_PROVIDER


async def _select_payment_provider(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    message = update.message
    subscription_id = context.user_data['subscription:id']
    subscription_condition_id = context.user_data['subscription:condition_id']
    if message.text == strings.get_string('back_button', user.language):
        await send_subscription_conditions(update, subscription_id, user, context)
        return CHOOSE_CONDITION
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    payment_provider_name = message.text
    payment_provider = payment_providers.get_payment_provider_by_name(payment_provider_name)
    if payment_provider is None:
        await update.message.reply_text(strings.get_string('provider_provider_not_supported', user.language))
        return SELECT_PAYMENT_PROVIDER
    exchanged_price = currency_exchange_service.convert_usd_to_uzs(subscription_condition.price)
    payment = await payments_repository.save_payment(
        int(exchanged_price),
        payment_provider.name,
        user.id,
        subscription_id,
        subscription_condition_id
    )
    if payment_provider.name == 'Fake':
        await payments_repository.set_status(payment.id, PaymentStatus.CONFIRMED)
        await subscriptions_repository.add_subscription_to_user(subscription.id, subscription_condition.id, user.telegram_user_id)
        telegram_group_ids = subscription.telegram_group_ids.split(',')
        telegram_user_id = user.telegram_user_id
        invite_links = []
        index_group_mapper = {
            0: {
                'ru': 'Амаля',
                'uz': 'Amal'
            },
            1: {
                'ru': 'Захриддина',
                'uz': 'Zahridin'
            }
        }
        for index, telegram_group_chat_id in enumerate(telegram_group_ids):
            chat_member = await context.bot.get_chat_member(telegram_group_chat_id, telegram_user_id)
            if chat_member.status == 'kicked':
                await context.bot.unban_chat_member(telegram_group_chat_id, telegram_user_id)
            invite_link = await context.bot.export_chat_invite_link(telegram_group_chat_id)
            link_name = f"[{strings.get_string('invite_group', user.language)}]" if len(
                telegram_group_ids) == 1 else f"[{strings.get_string('invite_group', user.language).format(name=index_group_mapper[index][user.language])}]"
            invite_links.append(f"<a href='{invite_link}'>{link_name}</a>")
        await context.bot.send_message(user.telegram_user_id,
                                       strings.get_string('subscription_purchased', user.language).format(
                                           invite_links=' '.join(invite_links)),
                                       parse_mode=ParseMode.HTML,
                                       reply_markup=ReplyKeyboardRemove())
        await update.message.reply_video_note('DQACAgIAAxkDAAIDtWWMf8vD6t_meoDEAT0oa-Xpedm0AAIlRQACT7BpSAgX2xXgIQ4JMwQ')
        await update.message.reply_video('BAACAgIAAxkDAAIDtmWMf84VTJyg7MnggOa8CwJA-HQFAAJpRQACFG1hSPkMCYQ7fdlFMwQ')
        await update.message.reply_video('BAACAgIAAxkDAAIDt2WMf9KV0uH1yVSNdWtj39y7t2xYAAIoRQACT7BpSMAcZXLoo9ZDMwQ')
        return ConversationHandler.END
    if payment_provider.name == 'Click':
        try:
            payment_provider.create_invoice(int(exchanged_price), user.phone, payment.id)
            await update.message.reply_text(
                f'Вам выставлен счёт в системе {payment_provider.name}. Оплатите его и вам будет оформлена подписка')
        except Exception as e:
            await update.message.reply_text(
                f'Ошибка при создании платежа в системе {payment_provider.name}. Обратитесь к разработчику.\n\nДля перезапуска бота, отправьте команду /start')
            raise e
    elif payment_provider.name == 'Payme':
        payment_url = payment_provider.get_payment_url(int(exchanged_price), subscription.name, payment.id)
        await update.message.reply_text(f"Оплатите через систему {payment_provider.name}",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                            strings.get_string('subscription_pay', user.language), url=payment_url)]]))
    elif payment_provider.name == 'Cloud Payments':
        await update.message.reply_text(
            f"Оплатите через систему {payment_provider.name}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(strings.get_string('subscription_pay', user.language),
                                      url=f'https://api-bot.onepayment.uz/webapp/?payment_id={payment.id}'
                                          f'&language={user.language}'
                                          f'&amount={int(exchanged_price)}'
                                          f'&subscription_name={subscription.name}'
                                          f'&user_id={user.id}'
                                          f'&subscription_id={subscription.id}'
                                          f'&subscription_condition_id={subscription_condition_id}'
                                      )
                 ],
            ])
        )
    back_message = await context.bot.send_message(update.effective_chat.id,
                                                  strings.get_string('payment_cancelation_button', user.language),
                                                  reply_markup=ReplyKeyboardMarkup(
                                                      [[strings.get_string('back_button', user.language)]],
                                                      resize_keyboard=True))
    context.user_data['back_message_id'] = back_message.message_id

    return BACK


async def _back_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    subscription_id = context.user_data['subscription:id']
    subscription_condition_id = context.user_data['subscription:condition_id']
    await send_payment_providers(update, context, subscription_id, subscription_condition_id, user)

    return SELECT_PAYMENT_PROVIDER


async def cloud_payment_web_app_data(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.effective_message.web_app_data is None:
        return await _back_handler(update, context)
    data = json.loads(update.effective_message.web_app_data.data)
    logging.info('Received web app data %r', data)
    if 'cloud_payment' not in data:
        return await _back_handler(update, context)
    subscription_id = context.user_data['subscription:id']
    subscription_condition_id = context.user_data['subscription:condition_id']
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    service = cloud_payments.CloudPaymentApi()
    if not service.test_connection():
        await update.message.reply_text('Сервис Cloud Payments сейчас недоступен, пожалуйста, выберите другой сервис')
        return await _back_handler(update, context)
    result = service.charge(
        amount=subscription_condition.price,
        currency='USD',
        ip_address=data['ip_address'],
        card_cryptogram_packet=data['cryptogram'],
        payment_id=data['payment_id'],
        card_holder_name=data['name'] if 'name' in data else None
    )
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    if result['status'] == 'success':
        await subscriptions_repository.add_subscription_to_user(subscription_id, subscription_condition_id, user.id)
        await payments_repository.set_status(data['payment_id'], PaymentStatus.CONFIRMED)
        await update.message.reply_text(strings.get_string('subscription_purchased', user.language))
    elif result['status'] == '3d_secure':
        result_data = result['data']
        await update.message.reply_text(
            'Нажмите на кнопку, чтобы выполнить 3D Secure',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    '3D Secure',
                    url=f'http://localhost:8000/api/payments/cloud-payments/pre-3d-secure?acs_url={result_data["acs_url"]}&md={result_data["transaction_id"]}&pa_req={result_data["pa_req"]}'
                )]]
            )
        )
        await payments_repository.set_clouds_payments_transaction_id(data['payment_id'], result_data["transaction_id"])
        await payments_repository.set_status(data['payment_id'], PaymentStatus.WAITING)
    else:
        # rejected
        data = result['data']
        await update.message.reply_html(
            f'Оплата не прошла\n\n<b>Код ошибки:</b> <code>{data["reason_code"]}</code>\n<b>Ошибка:</b> {data["reason"]}\n<b>Сообщение:</b> {data["message"]}')


async def _fallbacks_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.pre_checkout_query:
        await handlers._pre_checkout_subscription(update, context)
    return ConversationHandler.END


handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[MessageHandler(
        filters.Text('OneZone [RU] группа - аналитические сигналы') |
        filters.Text('OneZone [RU][UZ] группа - аналитические сигналы') |
        filters.Text('OneZone [UZ] группа - аналитические сигналы'),
        _subscription_start)],
    states={
        CHOOSE_SUBSCRIPTION: [MessageHandler(filters.TEXT, _choose_subscription)],
        CHOOSE_CONDITION: [MessageHandler(filters.TEXT, _choose_condition)],
        SELECT_PAYMENT_PROVIDER: [MessageHandler(filters.TEXT, _select_payment_provider)],
        CLOUD_PAYMENTS: [MessageHandler(filters.StatusUpdate.WEB_APP_DATA | filters.TEXT, cloud_payment_web_app_data)],
        BACK: [MessageHandler(filters.TEXT, _back_handler)]
    },
    fallbacks=[registration_handler, MessageHandler(filters.TEXT, _fallbacks_handler)]
)
