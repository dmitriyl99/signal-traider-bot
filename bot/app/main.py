import logging

from telegram.ext import ApplicationBuilder, CallbackContext, MessageHandler, filters
from telegram.constants import ChatType
from telegram import Update, ReplyKeyboardRemove

from app.conversations import registration_conversation, select_subscription_conversation, language_conversation, renew_subscription
from app.payments import handlers as payment_handlers
from app.config import config


async def default_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
        if update.message.new_chat_members or update.message.left_chat_member:
            await update.message.delete()
    if update.message.chat.type != ChatType.PRIVATE:
        return
    await update.message.reply_text("Отправьте команду /start для перезапуска бота", reply_markup=ReplyKeyboardRemove())


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(registration_conversation.handler)
    application.add_handler(select_subscription_conversation.handler)
    application.add_handler(language_conversation.handler)
    application.add_handlers(payment_handlers.handlers)
    application.add_handler(renew_subscription.handler)
    application.add_handler(MessageHandler(filters.ALL, default_handler))
    if config.ENV == 'production':
        application.run_webhook(
            listen='0.0.0.0',
            port=config.WEBHOOK_PORT,
            url_path=f'api/telegram-update/{config.WEBHOOK_TOKEN}',
            webhook_url=f'https://service-bot.onepayment.uz/api/telegram-update/{config.WEBHOOK_TOKEN}'
        )
    else:
        application.run_polling()


if __name__ == '__main__':
    main()
