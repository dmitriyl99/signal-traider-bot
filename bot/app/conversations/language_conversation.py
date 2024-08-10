from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.constants import ChatType
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

from app.resources import strings
from app.data.db import users_repository
from app.conversations.registration_conversation import handler as registration_handler

LANGUAGE = range(1)


async def _start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.message.chat.type != ChatType.PRIVATE:
        return ConversationHandler.END
    current_user = await users_repository.get_user_by_telegram_id(update.effective_user.id)
    if not current_user:
        return ConversationHandler.END
    await update.message.reply_text(strings.get_string('registration_language'),
                                    reply_markup=ReplyKeyboardMarkup(
                                        keyboard=[[
                                            '🇺🇿 Узбек',
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
    result = await users_repository.set_user_language(update.effective_user.id, languages[text])
    if not result:
        return ConversationHandler.END
    await update.message.reply_text(strings.get_string('language_changed', languages[text]), reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def _fallbacks_text(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("Что-то пошло не так. Отправьте команду /lang, чтобы перезапустить бота")
    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[CommandHandler('lang', _start)],
    states={
        LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, _language)],
    },
    fallbacks=[
        CommandHandler('lang', _start),
        registration_handler,
        MessageHandler(filters.TEXT, _fallbacks_text),
    ]
)
