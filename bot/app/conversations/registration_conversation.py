from typing import Optional
import logging

from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, helpers
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

from app.resources import strings
from app.data.models.subscription import SubscriptionUser
from app.data.models.users import User
from app import actions
from app.data.db import users_repository, subscriptions_repository, utm_respository
from app.helpers import date
from app.services.otp_service import OTPService
from app.services import masspay

NAME, PHONE, OTP = range(3)


async def _start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    await _process_update_for_utm(update)
    hash_command_user = await _process_update_for_hash_command(update, context)
    if hash_command_user:
        active_subscription: SubscriptionUser = await subscriptions_repository.get_active_subscription_for_user(
            hash_command_user)
        if active_subscription is not None:
            await actions.send_current_subscription_information(active_subscription, update)
            return ConversationHandler.END
    current_user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    if current_user is not None:
        await update.message.reply_text(strings.hello_message % current_user.name)
        if current_user.verified_at is None:
            otp_service = OTPService(current_user.phone)
            otp_service.send_otp()
            context.user_data['registration_phone'] = current_user.phone
            await update.message.reply_text(
                'Вы ещё не потвердили свой номер телефона. Мы отправили вам смс с кодом, пожалуйста, введите его')
            return OTP
        await users_repository.activate_proactively_added_user(current_user.phone, current_user.telegram_user_id)
        active_subscription: SubscriptionUser = await subscriptions_repository.get_active_subscription_for_user(
            current_user)
        if active_subscription is not None:
            await actions.send_current_subscription_information(active_subscription, update)
            return ConversationHandler.END
        await actions.send_subscription_menu_button(update, context)
        return ConversationHandler.END
    await update.message.reply_text(strings.registration_name, reply_markup=ReplyKeyboardRemove())

    return NAME


async def _name(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    text = update.message.text
    context.user_data['registration_name'] = text.strip().replace('\n', '')
    keyboard = [[KeyboardButton(text=strings.send_phone_button_text, request_contact=True)]]

    if 'registration_phone' in context.user_data:
        if 'hash_command_subscription_id' in context.user_data:
            user = await users_repository.save_user(context.user_data['registration_name'],
                                                    context.user_data['registration_phone'], update.effective_user.id)
            await users_repository.verify_user(user.id)
            subscription = (await subscriptions_repository.get_subscriptions())[0]
            active_subscription = await subscriptions_repository.add_subscription_with_days_to_user(user,
                                                                                                    subscription.id,
                                                                                                    context.user_data[
                                                                                                        'hash_command_subscription_days'])
            await update.message.reply_text(
                text='Вы активировали бонусную подписку!'
            )
            await actions.send_current_subscription_information(active_subscription, update)
            return ConversationHandler.END

    await update.message.reply_text(
        strings.registration_phone,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='HTML'
    )
    return PHONE


async def _phone(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    if update.message.contact is not None:
        phone_number = update.message.contact.phone_number
        phone_number = phone_number.replace('+', '')
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
            await update.message.reply_text(strings.validation_phone_message)
            return PHONE
    existed_user = await users_repository.find_user_by_phone(phone_number)
    if existed_user is not None:
        if existed_user.telegram_user_id is not None:
            await update.message.reply_text('Пользовтаель с этим номером телефона уже существует')
            return

    otp_service = OTPService(phone_number)
    otp_service.send_otp()
    keyboard = [[KeyboardButton(text=strings.wrong_number_button_text)]]
    await update.message.reply_text(
        'Мы отправили вам на номер смс с кодом, пожалуйста, подтвердите свой номер телефона',
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    context.user_data['registration_phone'] = phone_number
    return OTP


async def _verify_otp(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    if update.message.text == strings.wrong_number_button_text:
        keyboard = [[KeyboardButton(text=strings.send_phone_button_text, request_contact=True)]]

        await update.message.reply_text(
            strings.registration_phone,
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
            parse_mode='HTML'
        )

        return PHONE

    otp_service = OTPService(context.user_data['registration_phone'])
    if not update.message.text.isnumeric():
        await update.message.reply_text('Вы отправили неверный формат OTP')
        return OTP
    otp_verification_result = otp_service.verify_otp(int(update.message.text))
    if not otp_verification_result:
        await update.message.reply_text('Вы отправили неверный OTP')
        return OTP

    user = await users_repository.save_user(context.user_data['registration_name'], context.user_data['registration_phone'], update.effective_user.id)
    await users_repository.verify_user(user.id)
    await users_repository.activate_proactively_added_user(context.user_data['registration_phone'],
                                                           update.effective_user.id)
    await update.message.reply_text(strings.registration_finished, reply_markup=ReplyKeyboardRemove())
    active_subscription: SubscriptionUser = await subscriptions_repository.get_active_subscription_for_user(user)
    if active_subscription is None:
        await actions.send_subscription_menu_button(update, context)
    else:
        await actions.send_current_subscription_information(active_subscription, update)
    del context.user_data['registration_name']
    return ConversationHandler.END


async def _fallbacks_text(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("Что-то пошло не так. Отправьте команду /start, чтобы перезапустить бота")
    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[CommandHandler('start', _start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, _name)],
        PHONE: [MessageHandler((filters.TEXT | filters.CONTACT) & ~filters.COMMAND, _phone)],
        OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, _verify_otp)]
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


async def _process_update_for_hash_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> Optional[User]:
    logging.info(f'Process for hash command: {update.message.text}')
    text = update.message.text
    if '/start' not in text:
        return None
    text_split = text.split(' ')
    if len(text_split) == 1:
        return None
    payload = text_split[1]
    if 'hash' not in payload:
        return None
    logging.info(f'Hash found for user {update.effective_user.id}')
    hash_payload_split = payload.split('_')
    if len(hash_payload_split) == 1:
        return None
    hash_command = hash_payload_split[1]
    result: masspay.CheckHashCommandResult = masspay.check_hash_command(hash_command)
    if result is None:
        return None

    subscriptions = await subscriptions_repository.get_subscriptions()
    subscription = subscriptions[0]
    existing_user_by_phone = await users_repository.find_user_by_phone(result.user_phone_number)
    if existing_user_by_phone:
        if update.effective_user.id != existing_user_by_phone.telegram_user_id:
            return None
        await subscriptions_repository.add_subscription_with_days_to_user(existing_user_by_phone, subscription.id,
                                                                          result.subscription_days)
        return existing_user_by_phone
    context.user_data['registration_phone'] = result.user_phone_number
    context.user_data['hash_command_subscription_id'] = subscription.id
    context.user_data['hash_command_subscription_days'] = result.subscription_days

    return None
