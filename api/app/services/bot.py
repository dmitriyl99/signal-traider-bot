import aiogram.utils.exceptions
import logging
from typing import Optional, BinaryIO, List, Dict, Any
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
    signals_repository.save_mapper_for_signal(signal, chat_message_mapper)


async def send_text_distribution(text: str, attachments: Optional[List[Dict[str, Any]]], user_repository: UsersRepository, admin_user: AdminUser, importance: int, currency: str | None):
    if len(list(filter(lambda x: x.name == 'Analyst', admin_user.roles))) > 0:
        users = await user_repository.get_all_users_with_active_subscriptions(analyst_id=admin_user.id)
    else:
        users = await user_repository.get_all_users_with_active_subscriptions()
    logging.info(f'Send text message to {len(users)} users')
    users_chunks = array.chunks(users, 50)
    for chunk in users_chunks:
        for user in chunk:
            await send_message_to_user(
                user.telegram_user_id, text, attachments, importance=importance, currency=currency
            )


async def send_message_to_user(
        telegram_user_id: int,
        text: str = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        reply_to_message_id: int = None,
        importance: int = 0,
        currency: str | None = None,
        remove_keyboard: bool = False
) -> Optional[types.Message] | Optional[List[types.Message]]:
    bot = Bot(settings.telegram_bot_api_token)
    reply_keyboard = None
    if remove_keyboard:
        reply_keyboard = types.ReplyKeyboardRemove()
    if text == 'null':
        text = None
    if currency:
        text = f"<b>{currency}</b>\n\n" + text
    if text:
        if importance == 1:
            text = '❗ ' + text
        elif importance >= 2:
            text = '❗️❗️❗️ ' + text
    if attachments is not None and len(attachments) > 0:
        files = attachments
        try:
            if len(files) == 1:
                file: BinaryIO = files[0]['binary']
                content_type = files[0]['type']
                is_image = files[0]['is_image']
                file.seek(0)
                bio = BytesIO(file.read())
                if not is_image:
                    return await bot.send_document(
                        chat_id=telegram_user_id,
                        reply_markup=reply_keyboard,
                        document=types.InputFile(bio, filename=files[0]['filename']),
                        caption=text if text else '',
                        parse_mode=types.ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                if 'image' in content_type:
                    return await bot.send_photo(
                        chat_id=telegram_user_id,
                        reply_markup=reply_keyboard,
                        photo=types.InputFile(bio, filename=files[0]['filename']),
                        caption=text if text else '',
                        parse_mode=types.ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                elif 'video' in content_type:
                    return await bot.send_video(
                        chat_id=telegram_user_id,
                        reply_markup=reply_keyboard,
                        video=types.InputFile(bio, filename=files[0]['filename']),
                        caption=text if text else '',
                        parse_mode=types.ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                else:
                    return await bot.send_document(
                        chat_id=telegram_user_id,
                        reply_markup=reply_keyboard,
                        document=types.InputFile(bio, filename=files[0]['filename']),
                        caption=text if text else '',
                        parse_mode=types.ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
            else:
                media_group = types.MediaGroup()
                for idx, f in enumerate(files):
                    binary = f['binary']
                    content_type = f['type']
                    is_image = files[0]['is_image']
                    binary.seek(0)
                    bio = BytesIO(binary.read())
                    if not is_image:
                        media_group.attach_document(
                            types.InputFile(bio, filename=f['filename']),
                            caption=text if idx == 0 and text else '',
                            parse_mode=types.ParseMode.HTML,
                        )
                    if 'image' in content_type:
                        media_group.attach_photo(
                            types.InputFile(bio, filename=f['filename']),
                            caption=text if idx == 0 and text else '',
                            parse_mode=types.ParseMode.HTML,
                        )
                    elif 'video' in content_type:
                        media_group.attach_video(
                            types.InputFile(bio, filename=f['filename']),
                            caption=text if idx == 0 and text else '',
                            parse_mode=types.ParseMode.HTML,
                        )
                    else:
                        media_group.attach_document(
                            types.InputFile(bio, filename=f['filename']),
                            caption=text if idx == 0 and text else '',
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
        message = await bot.send_message(
            telegram_user_id,
            text,
            parse_mode=types.ParseMode.HTML,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_keyboard
        )
        return message
    except aiogram.utils.exceptions.ChatNotFound:
        return None
    except aiogram.utils.exceptions.BotBlocked:
        return None
    except Exception as e:
        await bot.send_message(76777495, f"Error while sending message to user {telegram_user_id}: {e}")
        return None
