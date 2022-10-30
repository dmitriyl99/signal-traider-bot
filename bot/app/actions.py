from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.data.db import subscriptions_repository

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
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
                [KeyboardButton(strings.get_string('choose_subscription_text', user.language), callback_data='choose_subscription')]
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
        days=diff_days
        )
    )


async def send_subscriptions(update: Update):
    subscriptions = await subscriptions_repository.get_subscriptions()
    chunked_subscriptions = array.chunks(subscriptions, 2)
    keyboard = []
    for chunk in chunked_subscriptions:
        buttons = []
        for subscription in chunk:
            buttons.append(
                KeyboardButton(subscription.name))
        keyboard.append(buttons)
    await update.message.reply_text('Выберите подписку', reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


async def send_subscription_conditions(update: Update, subscription_id: int):
    subscription_conditions = await subscriptions_repository.get_subscription_condition(subscription_id)
    chunked_conditions = array.chunks(subscription_conditions, 2)
    keyboard = []
    for chunk in chunked_conditions:
        buttons = []
        for condition in chunk:
            buttons.append(
                KeyboardButton('%s месяц' % condition.duration_in_month))
        keyboard.append(buttons)
    keyboard.append([KeyboardButton('Назад')])
    await update.message.reply_text('Выберите срок подписки', reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


async def send_payment_providers(update: Update, context: CallbackContext.DEFAULT_TYPE, subscription_id, subscription_condition_id):
    message = update.message
    providers = payment_providers.get_payment_providers()
    subscription = await subscriptions_repository.get_subscription_by_id(subscription_id)
    subscription_condition = list(filter(lambda sc: sc.id == subscription_condition_id, subscription.conditions))[0]
    keyboard_buttons = list(map(
        lambda provider: KeyboardButton(provider.name,),
        providers))
    await message.reply_text(text='<b>Подписка:</b> {}\n<b>Срок:</b> {}\n<b>Цена:</b> ${}'.format(
        subscription.name,
        subscription_condition.duration_in_month,
        int(subscription_condition.price / 100)
    ), reply_markup=ReplyKeyboardMarkup([keyboard_buttons, [KeyboardButton('Назад')]], resize_keyboard=True), parse_mode='HTML')
