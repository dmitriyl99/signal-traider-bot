from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from app.resources import strings


def send_subscription_menu_button(update: Update, context: CallbackContext.DEFAULT_TYPE):
    return update.message.reply_text(
        strings.subscription_menu_message,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(strings.choose_subscription_text, callback_data='choose_subscription')]
            ]
        )
    )
