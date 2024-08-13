from typing import Optional
import logging

from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.constants import ChatType, ChatAction, ParseMode
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

from app.config import config
from app.data.models.payments import PaymentStatus
from app.resources import strings
from app.data.models.subscription import SubscriptionUser
from app import actions
from app.payments import providers as payment_providers, handlers
from app.data.db import users_repository, subscriptions_repository, utm_respository, payments_repository
from app.services import currency_exchange as currency_exchange_service
from app.services.otp_service import OTPService

LANGUAGE, NAME, PHONE, OTP, CHOOSE_SUBSCRIPTION, CHOOSE_CONDITION, SELECT_PAYMENT_PROVIDER, BACK = range(8)


async def _start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.message.chat.type != ChatType.PRIVATE:
        return ConversationHandler.END
    await _process_update_for_utm(update)
    # hash_command_user = await _process_update_for_hash_command(update, context)
    # if hash_command_user:
    #     active_subscription: SubscriptionUser = await subscriptions_repository.get_active_subscription_for_user(
    #         hash_command_user)
    #     if hash_command_user.language is None:
    #         await update.message.reply_text(strings.get_string('registration_language'),
    #                                         reply_markup=ReplyKeyboardMarkup(
    #                                             keyboard=[[
    #                                                 '🇷🇺 Русский',
    #                                                 "🇺🇿 O'zbek"]], resize_keyboard=True))
    #
    #         return LANGUAGE
    #     if active_subscription is not None:
    #         await actions.send_current_subscription_information(active_subscription, update, hash_command_user, context)
    #         return ConversationHandler.END
    current_user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    if current_user is not None:
        if current_user.language is None:
            await update.message.reply_text(strings.get_string('registration_language'),
                                            reply_markup=ReplyKeyboardMarkup(
                                                keyboard=[[
                                                    '🇺🇿 Ўзбек',
                                                    "🇺🇿 O'zbek"]], resize_keyboard=True))

            return LANGUAGE
        await update.message.reply_text(strings.get_string('hello_message', current_user.language) % current_user.name)
        if current_user.verified_at is None:
            otp_service = OTPService(current_user.phone)
            otp_service.send_otp()
            context.user_data['registration_phone'] = current_user.phone
            keyboard = [
                [
                    KeyboardButton(text=strings.get_string('wrong_number_button_text',
                                                           current_user.language))
                ]
            ]
            context.user_data['registration_language'] = current_user.language
            await update.message.reply_text(
                strings.get_string('registration_phone_not_verified', current_user.language),
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
            return OTP
        await users_repository.activate_proactively_added_user(current_user.phone, current_user.telegram_user_id)
        active_subscription: SubscriptionUser = await subscriptions_repository.get_active_subscription_for_user(
            current_user)
        if active_subscription is not None:
            await actions.send_current_subscription_information(active_subscription, update, current_user, context)
            return ConversationHandler.END
        await actions.send_subscription_conditions(update, 1, current_user, context)
        return CHOOSE_CONDITION
    await update.message.reply_text(strings.get_string('registration_language'),
                                    reply_markup=ReplyKeyboardMarkup(keyboard=[[
                                        '🇺🇿 Ўзбек',
                                        "🇺🇿 O'zbek"]], resize_keyboard=True))

    return LANGUAGE


async def _language(update: Update, context: CallbackContext.DEFAULT_TYPE):
    text = update.message.text
    languages = {
        '🇺🇿 Ўзбек': 'ўз',
        "🇺🇿 O'zbek": 'uz'
    }
    if text not in languages:
        await update.message.reply_text(strings.get_string('registration_language_wrong'))
        return LANGUAGE
    current_user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    context.user_data['registration_language'] = languages[text]
    if current_user is not None:
        await users_repository.set_user_language(update.effective_user.id, languages[text])
        return await _start(update, context)
    # await update.message.reply_html(strings.get_string('welcome_text'), context.user_data['registration_language'],
    #                                 reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(strings.get_string('registration_name', context.user_data['registration_language']),
                                    reply_markup=ReplyKeyboardRemove())

    return NAME


async def _name(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    text = update.message.text
    context.user_data['registration_name'] = text.strip().replace('\n', '')
    keyboard = [[KeyboardButton(
        text=strings.get_string('send_phone_button_text', language=context.user_data['registration_language']),
        request_contact=True)]]

    if 'registration_phone' in context.user_data:
        if 'hash_command_subscription_id' in context.user_data:
            user = await users_repository.save_user(context.user_data['registration_name'],
                                                    context.user_data['registration_phone'], update.effective_user.id,
                                                    language=context.user_data['registration_language'])
            await users_repository.verify_user(user.id)
            subscription = (await subscriptions_repository.get_subscriptions())[0]
            active_subscription = await subscriptions_repository.add_subscription_with_days_to_user(user,
                                                                                                    subscription.id,
                                                                                                    context.user_data[
                                                                                                        'hash_command_subscription_days'])
            await update.message.reply_text(
                text=strings.get_string('registration_bonus_activated', user.language)
            )
            await actions.send_current_subscription_information(active_subscription, update, user, context)
            return ConversationHandler.END

    await update.message.reply_text(
        strings.get_string('registration_phone', context.user_data['registration_language']),
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='HTML'
    )
    return PHONE


async def _phone(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    if update.message.contact is not None:
        dirty_phone_number = update.message.contact.phone_number
        phone_number = dirty_phone_number.replace('+', '')
    else:
        # regex = r'\+*998\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}'
        # pattern = re.compile(regex)
        # match = re.search(pattern, update.message.text)
        # if match is None:
        #     await update.message.reply_text(strings.validation_phone_message)
        #     return PHONE
        dirty_phone_number = update.message.text
        un_spaced_phone_number = dirty_phone_number.replace(' ', '')
        phone_number = un_spaced_phone_number.replace('+', '')
        if not phone_number.isnumeric():
            await update.message.reply_text(
                strings.get_string('validation_phone_message', context.user_data['registration_language']))
            return PHONE
    existed_user = await users_repository.find_user_by_phone(phone_number)
    if existed_user is not None:
        if existed_user.telegram_user_id and existed_user.telegram_user_id != update.effective_user.id:
            await update.message.reply_text(
                strings.get_string('registration_phone_user_exists', context.user_data['registration_language']))
            return

    otp_service = OTPService(phone_number)
    otp_service.send_otp()
    keyboard = [
        [
            KeyboardButton(text=strings.get_string('wrong_number_button_text',
                                                   context.user_data['registration_language']))
        ]
    ]
    await update.message.reply_text(
        strings.get_string('registration_phone_otp_sent', context.user_data['registration_language']),
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    context.user_data['registration_phone'] = phone_number
    return OTP


async def _verify_otp(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.message.text == strings.get_string('wrong_number_button_text',
                                                 context.user_data['registration_language']):
        keyboard = [[KeyboardButton(
            text=strings.get_string('send_phone_button_text', context.user_data['registration_language']),
            request_contact=True)]]

        await update.message.reply_text(
            strings.get_string('registration_phone', context.user_data['registration_language']),
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
            parse_mode='HTML'
        )

        return PHONE

    otp_service = OTPService(context.user_data['registration_phone'])
    if not update.message.text.isnumeric():
        await update.message.reply_text(
            strings.get_string('registration_phone_otp_wrong_format', context.user_data['registration_language']))
        return OTP
    otp_verification_result = otp_service.verify_otp(int(update.message.text))
    if not otp_verification_result:
        await update.message.reply_text(
            strings.get_string('registration_phone_otp_wrong', context.user_data['registration_language']))
        return OTP

    user = await users_repository.find_user_by_phone(context.user_data['registration_phone'])
    if user is None:
        user = await users_repository.save_user(
            context.user_data['registration_name'],
            context.user_data['registration_phone'],
            update.effective_user.id,
            context.user_data['registration_language']
        )
    await users_repository.verify_user(user.id)
    # amocrm_integration.add_user_to_catalog(user, amocrm_integration.AmoCrmUserType.NEW_USER)
    await users_repository.activate_proactively_added_user(context.user_data['registration_phone'],
                                                           update.effective_user.id,
                                                           context.user_data['registration_language'])
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    await users_repository.activate_proactively_added_user(context.user_data['registration_phone'],
                                                           update.effective_user.id)
    await update.message.reply_text(strings.get_string('registration_finished', user.language),
                                    reply_markup=ReplyKeyboardRemove())
    active_subscription: SubscriptionUser = await subscriptions_repository.get_active_subscription_for_user(user)
    if active_subscription is None:
        await actions.send_subscription_conditions(update, 1, user, context)
        return CHOOSE_CONDITION
    else:
        await actions.send_current_subscription_information(active_subscription, update, user, context)
    if 'registration_name' in context.user_data:
        del context.user_data['registration_name']
    return ConversationHandler.END


async def _choose_condition(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)

    async def error():
        await update.message.reply_text(strings.get_string('subscription_condition_wrong', user.language))
        return CHOOSE_CONDITION

    message = update.message
    # In this action need to send payment invoice, but for now without
    message_data = message.text
    if strings.get_string('back_button', user.language) in message_data:
        await actions.send_subscriptions(update, context, user)
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

    await actions.send_payment_providers(update, context, subscription_id, subscription_condition_id, user)

    return SELECT_PAYMENT_PROVIDER


async def _select_payment_provider(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    message = update.message
    subscription_id = context.user_data['subscription:id']
    subscription_condition_id = context.user_data['subscription:condition_id']
    if message.text == strings.get_string('back_button', user.language):
        await actions.send_subscription_conditions(update, subscription_id, user, context)
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
        telegram_user_id = user.telegram_user_id
        invite_links = []
        telegram_group_chat_id = config.TELEGRAM_GROUP_ID
        # for index, telegram_group_chat_id in enumerate(telegram_group_ids):
        chat_member = await context.bot.get_chat_member(telegram_group_chat_id, telegram_user_id)
        if chat_member.status == 'kicked':
            await context.bot.unban_chat_member(telegram_group_chat_id, telegram_user_id)
        invite_link = await context.bot.export_chat_invite_link(telegram_group_chat_id)
        link_name = f"[{strings.get_string('invite_group', user.language).format(name='')}]"
        # link_name = f"[{strings.get_string('invite_group', user.language).format(name='')}]" if len(
        #     [telegram_group_chat_id]) == 1 else f"[{strings.get_string('invite_group', user.language).format(name=index_group_mapper[index][user.language])}]"
        invite_links.append(f"<a href='{invite_link}'>{link_name}</a>")
        await context.bot.send_message(user.telegram_user_id,
                                       strings.get_string('subscription_purchased', user.language).format(
                                           invite_links=' '.join(invite_links)),
                                       parse_mode=ParseMode.HTML,
                                       reply_markup=ReplyKeyboardRemove())
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
    await actions.send_payment_providers(update, context, subscription_id, subscription_condition_id, user)

    return SELECT_PAYMENT_PROVIDER


async def _fallbacks_text(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("Что-то пошло не так. Отправьте команду /start, чтобы перезапустить бота")
    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[CommandHandler('start', _start)],
    states={
        LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, _language)],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, _name)],
        PHONE: [MessageHandler((filters.TEXT | filters.CONTACT) & ~filters.COMMAND, _phone)],
        OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, _verify_otp)],
        CHOOSE_CONDITION: [MessageHandler(filters.TEXT, _choose_condition)],
        SELECT_PAYMENT_PROVIDER: [MessageHandler(filters.TEXT, _select_payment_provider)],
        BACK: [MessageHandler(filters.TEXT, _back_handler)]
    },
    fallbacks=[
        CommandHandler('start', _start),
        MessageHandler(filters.TEXT, _fallbacks_text)
    ]
)


async def _process_update_for_utm(update: Update):
    logging.info(f'Process for UTM: {update.message.text}')
    text = update.message.text
    if '/start' not in text:
        return
    text_split = text.split(' ')
    if len(text_split) == 1:
        return
    payload = text_split[1]
    if 'utm' not in payload:
        return
    utm_payload_split = payload.split('_')
    if len(utm_payload_split) == 1:
        return
    utm_commands = utm_payload_split[1:]
    for utm_command in utm_commands:
        await utm_respository.utm_click(utm_command, update.effective_user.id)

# async def _process_update_for_hash_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> Optional[User]:
#     logging.info(f'Process for hash command: {update.message.text}')
#     text = update.message.text
#     if '/start' not in text:
#         return None
#     text_split = text.split(' ')
#     if len(text_split) == 1:
#         return None
#     payload = text_split[1]
#     if 'hash' not in payload:
#         return None
#     logging.info(f'Hash found for user {update.effective_user.id}')
#     hash_payload_split = payload.split('_')
#     if len(hash_payload_split) == 1:
#         return None
#     hash_command = hash_payload_split[1]
#     result: masspay.CheckHashCommandResult = masspay.check_hash_command(hash_command)
#     if result is None:
#         return None
#
#     subscriptions = await subscriptions_repository.get_subscriptions()
#     subscription = subscriptions[0]
#     existing_user_by_phone = await users_repository.find_user_by_phone(result.user_phone_number)
#     if existing_user_by_phone:
#         if update.effective_user.id != existing_user_by_phone.telegram_user_id:
#             return None
#         await subscriptions_repository.add_subscription_with_days_to_user(existing_user_by_phone, subscription.id,
#                                                                           result.subscription_days)
#         return existing_user_by_phone
#     context.user_data['registration_phone'] = result.user_phone_number
#     context.user_data['hash_command_subscription_id'] = subscription.id
#     context.user_data['hash_command_subscription_days'] = result.subscription_days
#
#     return None
