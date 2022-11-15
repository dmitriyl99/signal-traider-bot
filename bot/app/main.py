import logging

from telegram.ext import ApplicationBuilder, CallbackContext, MessageHandler, filters
from telegram import Update

from app.conversations import registration_conversation, select_subscription_conversation
from app.payments import handlers as payment_handlers
from app.config import config


async def default_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("Отправьте команду /start для перезапуска бота")


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(registration_conversation.handler)
    application.add_handler(select_subscription_conversation.handler)
    application.add_handlers(payment_handlers.handlers)
    application.add_handler(MessageHandler(filters.TEXT, default_handler))
    if config.ENV == 'production':
        application.run_webhook(
            listen='0.0.0.0',
            port=config.WEBHOOK_PORT,
            url_path=f'api/telegram-update/{config.WEBHOOK_TOKEN}',
            webhook_url=f'https://apibot.masspay.uz/api/telegram-update/{config.WEBHOOK_TOKEN}'
        )
    else:
        application.run_polling()


if __name__ == '__main__':
    main()
