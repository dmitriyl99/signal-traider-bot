import aiogram.utils.exceptions
import logging
from typing import Optional, BinaryIO, List
from io import BytesIO

from aiogram import Bot, types

from app.data.models.signal import Signal
from app.data.models.admin_users import AdminUser
from app.data.db.users_repository import UsersRepository
from app.data.db.signals_repository import SignalsRepository
from app.config import settings
from app.helpers import array


async def send_distribution(signal: Signal, user_repository: UsersRepository, signals_repository: SignalsRepository, admin_user: AdminUser):
    if len(list(filter(lambda x: x.name == 'Analyst', admin_user.roles))) > 0:
        users = await user_repository.get_all_users_with_active_subscriptions(admin_user.id)
    else:
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

    chat_message_mapper = {}

    for chunk in users_chunks:
        for user in chunk:
            message = await send_message_to_user(user.telegram_user_id, text)
            if message is list:
                continue
            if message is None:
                continue
            chat_message_mapper[user.telegram_user_id] = message.message_id
    print('chat_message_mapper: ', chat_message_mapper)
    signals_repository.save_mapper_for_signal(signal, chat_message_mapper)


async def send_text_distribution(text: str, files: Optional[List[BinaryIO]], user_repository: UsersRepository):
    users = await user_repository.get_all_users_with_active_subscriptions()
    logging.info(f'Send text message to {len(users)} users')
    users_chunks = array.chunks(users, 50)
    for chunk in users_chunks:
        for user in chunk:
            await send_message_to_user(user.telegram_user_id, text, files)


async def send_message_to_user(telegram_user_id: int, text: str, files: Optional[List[BinaryIO]] = None, reply_to_message_id: int = None) -> Optional[types.Message] | Optional[List[types.Message]]:
    bot = Bot(settings.telegram_bot_api_token)
    if files is not None:
        try:
            if len(files) == 1:
                file = files[0]
                file.seek(0)
                bio = BytesIO(file.read())
                return await bot.send_photo(
                    chat_id=telegram_user_id,
                    photo=types.InputFile(bio),
                    caption=text,
                    parse_mode=types.ParseMode.HTML,
                    reply_to_message_id=reply_to_message_id
                )
            else:
                media_group = types.MediaGroup()
                for idx, f in enumerate(files):
                    f.seek(0)
                    bio = BytesIO(f.read())
                    media_group.attach_photo(
                        types.InputFile(bio),
                        caption=text if idx == 0 else None,
                        parse_mode=types.ParseMode.HTML,
                    )
                return await bot.send_media_group(
                    telegram_user_id,
                    media=media_group,
                    reply_to_message_id=reply_to_message_id
                )
        except aiogram.utils.exceptions.ChatNotFound:
            return None
        except aiogram.utils.exceptions.BotBlocked:
            return None
        except Exception as e:
            return await bot.send_message(76777495, f"Error while sending message to user {telegram_user_id}: {e}")
    try:
        message = await bot.send_message(telegram_user_id, text, parse_mode=types.ParseMode.HTML, reply_to_message_id=reply_to_message_id)
        return message
    except aiogram.utils.exceptions.ChatNotFound:
        return None
    except aiogram.utils.exceptions.BotBlocked:
        return None
    except Exception as e:
        await bot.send_message(76777495, f"Error while sending message to user {telegram_user_id}: {e}")
        return None
