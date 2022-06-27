import os
import logging

from telegram.ext import ApplicationBuilder

from app.conversations import registration_conversation, select_subscription_conversation
from app.payments import handlers
from app.config import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

application.add_handler(registration_conversation.handler)
application.add_handler(select_subscription_conversation.handler)
application.add_handlers(handlers.handlers)

application.run_polling()
