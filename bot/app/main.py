import os
import logging

from telegram.ext import ApplicationBuilder

from app.conversations import registration_conversation, select_subscription_conversation
from app.payments import handlers
from app.config import config


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(registration_conversation.handler)
    application.add_handler(select_subscription_conversation.handler)
    application.add_handlers(handlers.handlers)
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
