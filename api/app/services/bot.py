import logging
from typing import Optional, BinaryIO, List
from io import BytesIO

from aiogram import Bot, types

from app.data.models.signal import Signal
from app.data.models.users import User
from app.data.db.users_repository import UsersRepository
from app.config import settings
from app.helpers import array


async def send_distribution(signal: Signal, user_repository: UsersRepository):
    users = await user_repository.get_all_users_with_active_subscriptions()
    logging.info(f'Send signal to {len(users)} users: {users}')
    users_chunks = array.chunks(users, 50)

    text = '<b>{currency_pair}</b> <b>{execution_method}</b> <b>{price}</b>'.format(currency_pair=signal.currency_pair,
                                                                                    execution_method=signal.execution_method,
                                                                                    price=signal.price)
    if signal.tr_1:
        text += '\n<b>TP 1</b>: {tr_1}'.format(tr_1=signal.tr_1)
    if signal.tr_2:
        text += '\n<b>TP 2</b>: {tr_2}'.format(tr_2=signal.tr_2)
    if signal.sl:
        text += '\n<b>SL</b>: {sl}'.format(sl=signal.sl)

    for chunk in users_chunks:
        for user in chunk:
            await send_message_to_user(user, text)


async def send_text_distribution(text: str, files: Optional[List[BinaryIO]], user_repository: UsersRepository):
    users = await user_repository.get_all_users_with_active_subscriptions()
    logging.info(f'Send text message to {len(users)} users')
    users_chunks = array.chunks(users, 50)
    for chunk in users_chunks:
        for user in chunk:
            await send_message_to_user(user, text, files)


async def send_message_to_user(user: User, text: str, files: Optional[List[BinaryIO]] = None):
    bot = Bot(settings.telegram_bot_api_token)
    if files is not None:
        await bot.send_media_group(
            user.telegram_user_id,
            media=types.MediaGroup(
                medias=[
                    types.InputMediaPhoto(
                        types.InputFile(
                            BytesIO(
                                f.read()
                            )
                        ), caption=text if idx == 1 else None, parse_mode=types.ParseMode.HTML) for idx, f in enumerate(files)]))
        return
    await bot.send_message(user.telegram_user_id, text, parse_mode=types.ParseMode.HTML)
