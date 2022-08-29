import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

from app.resources import strings
from app.data.models.subscription import SubscriptionUser
from app import actions
from app.data.db import users_repository, subscriptions_repository
from app.helpers import date

NAME, PHONE = range(2)


async def _start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    current_user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    if current_user is not None:
        await update.message.reply_text(strings.hello_message % current_user.name)
        await users_repository.check_for_proactively_added_user(current_user.phone, current_user.telegram_user_id)
        active_subscription: SubscriptionUser = await subscriptions_repository.get_active_subscription_for_user(current_user)
        if active_subscription is not None:
            subscription = await subscriptions_repository.get_subscription_by_id(active_subscription.subscription_id)
            now = datetime.now()
            subscription_end_date: datetime = active_subscription.created_at + relativedelta(days=active_subscription.duration_in_days)
            diff_days = date.diff_in_days(now, subscription_end_date)
            await update.message.reply_text(strings.active_subscription.format(
                name=subscription.name,
                to_date=subscription_end_date.strftime('%d.%m.%Y'),
                days=diff_days
                ),
            )
            return ConversationHandler.END
        await actions.send_subscription_menu_button(update, context)
        return ConversationHandler.END
    await update.message.reply_text(strings.registration_name, reply_markup=ReplyKeyboardRemove())

    return NAME


async def _name(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    text = update.message.text
    context.user_data['registration_name'] = text
    keyboard = [[KeyboardButton(text=strings.send_phone_button_text, request_contact=True)]]

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
        regex = r'\+*998\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}'
        pattern = re.compile(regex)
        match = re.search(pattern, update.message.text)
        if match is None:
            await update.message.reply_text(strings.validation_phone_message)
            return PHONE
        dirty_phone_number = match.group(0)
        un_spaced_phone_number = dirty_phone_number.replace(' ', '')
        phone_number = un_spaced_phone_number.replace('+', '')
    proactively_check_result = await users_repository.check_for_proactively_added_user(phone_number, update.effective_user.id)
    if proactively_check_result is True:
        await update.message.reply_text(strings.registration_proactively.format(name=context.user_data['registration_name']))
        await update.message.reply_text(strings.registration_finished, reply_markup=ReplyKeyboardRemove())
        del context.user_data['registration_name']
        return ConversationHandler.END
    await users_repository.save_user(context.user_data['registration_name'], phone_number, update.effective_user.id)
    await update.message.reply_text(strings.registration_finished, reply_markup=ReplyKeyboardRemove())
    await actions.send_subscription_menu_button(update, context)
    del context.user_data['registration_name']
    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[CommandHandler('start', _start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, _name)],
        PHONE: [MessageHandler((filters.TEXT | filters.CONTACT) & ~filters.COMMAND, _phone)]
    },
    fallbacks=[MessageHandler(filters.TEXT, '')]
)

