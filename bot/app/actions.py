from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.data.db import subscriptions_repository

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from app.data.models.subscription import SubscriptionUser
from app.data.models.users import User
from app.resources import strings
from app.helpers import date, array
from app.payments import providers as payment_providers


def send_subscription_menu_button(update: Update, context: CallbackContext.DEFAULT_TYPE, user: User):
    return update.message.reply_text(
        strings.get_string('subscription_menu_message', user.language),
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton(strings.get_string('graphical_signals', user.language))],
            ], resize_keyboard=True
        )
    )


async def send_current_subscription_information(active_subscription: SubscriptionUser, update: Update, user: User):
    subscription = await subscriptions_repository.get_subscription_by_id(active_subscription.subscription_id)
    now = datetime.now()
    subscription_end_date: datetime = active_subscription.created_at + relativedelta(
        days=active_subscription.duration_in_days)
    diff_days = date.diff_in_days(now, subscription_end_date)
    await update.message.reply_text(strings.get_string('active_subscription', user.language).format(
        name=subscription.name,
        to_date=subscription_end_date.strftime('%d.%m.%Y'),
        days=diff_days,
        ), reply_markup=ReplyKeyboardRemove()
    )


async def send_subscriptions(update: Update, context: CallbackContext.DEFAULT_TYPE, user: User):
    message_subscription_category_map = {
        strings.get_string('graphical_signals', 'ru'): 'graph_signals',
        strings.get_string('graphical_signals', 'uz'): 'graph_signals',
        strings.get_string('interday_subscriptions', 'ru'): 'interday',
        strings.get_string('marafon_subscriptions', 'ru'): 'marafon'
    }
    category = update.message.text
    if category not in message_subscription_category_map and 'current_subscription_category' in context.user_data:
        category = context.user_data['current_subscription_category']
    if category in message_subscription_category_map:
        category = message_subscription_category_map[category]
    context.user_data['current_subscription_category'] = category
    subscriptions = await subscriptions_repository.get_subscriptions(category=category)
    chunked_subscriptions = array.chunks(subscriptions, 2)
    keyboard = []
    for chunk in chunked_subscriptions:
        buttons = []
        for subscription in chunk:
            buttons.append(
                KeyboardButton(subscription.name))
        keyboard.append(buttons)
    keyboard.append([KeyboardButton(strings.get_string('back_button', user.language))])
    await update.message.reply_text(strings.get_string('choose_subscription_text', user.language),
                                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


async def send_subscription_conditions(update: Update, subscription_id: int, user: User):
    subscription_conditions = await subscriptions_repository.get_subscription_condition(subscription_id)
    chunked_conditions = array.chunks(subscription_conditions, 2)
    keyboard = []
    for chunk in chunked_conditions:
        buttons = []
        for condition in chunk:
            if condition.duration_in_month:
                buttons.append(
                    KeyboardButton(strings.get_string('subscription_condition_name_months',
                                                      user.language) % condition.duration_in_month))
            elif condition.duration_in_days:
                buttons.append(
                    KeyboardButton(strings.get_string('subscription_condition_name_days',
                                                      user.language) % condition.duration_in_days))
        keyboard.append(buttons)
    keyboard.append([KeyboardButton(strings.get_string('back_button', user.language))])
    await update.message.reply_text(strings.get_string('subscription_select_condition', user.language), reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


async def send_payment_providers(update: Update, context: CallbackContext.DEFAULT_TYPE, subscription_id, subscription_condition_id,  user: User):
    message = update.message
    providers = payment_providers.get_payment_providers()
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    keyboard_buttons = list(map(
        lambda provider: KeyboardButton(provider.name,),
        providers))
    await message.reply_text(text=strings.get_string('subscription_full_info', user.language).format(
        subscription.name,
        subscription_condition.duration_in_month if subscription_condition.duration_in_month else subscription_condition.duration_in_days,
        int(subscription_condition.price)
    ), reply_markup=ReplyKeyboardMarkup([keyboard_buttons, [KeyboardButton(strings.get_string('back_button', user.language))]], resize_keyboard=True), parse_mode='HTML')
