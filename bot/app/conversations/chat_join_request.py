from telegram.ext import ChatJoinRequestHandler, CallbackContext
from telegram import Update

from app.data.db import users_repository, subscriptions_repository
from app.data.models.subscription import SubscriptionUser


async def chat_join_request_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = await users_repository.get_user_by_telegram_id(update.chat_join_request.from_user.id)
    if not user:
        await update.chat_join_request.decline()
        return
    if user.verified_at is None:
        await update.chat_join_request.decline()
        return
    active_subscription: SubscriptionUser = await subscriptions_repository.get_active_subscription_for_user(user)
    if not active_subscription:
        await update.chat_join_request.decline()
        return
    await update.chat_join_request.approve()


handler = ChatJoinRequestHandler(chat_join_request_handler)
