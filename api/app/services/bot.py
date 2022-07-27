import requests
import logging

from app.data.models.signal import Signal
from app.data.models.users import User
from app.data.db.users_repository import UsersRepository
from app.config import settings
from app.helpers import array


async def send_distribution(signal: Signal, user_repository: UsersRepository):
    users = await user_repository.get_all_users_with_active_subscriptions()
    logging.info(f'Send signal to {len(users)} users: {users}')
    users_chunks = array.chunks(users, 50)

    text = """<b>{currency_pair}</b> <b>{execution_method}</b> <b>{price}</b>
<b>TR 1</b>: {tr_1}
<b>TR 2</b>: {tr_2}
<b>SL</b>: {sl}
    """.format(
        currency_pair=signal.currency_pair,
        execution_method=signal.execution_method,
        price=int(signal.price / 100),
        tr_1=signal.tr_1,
        tr_2=signal.tr_2,
        sl=signal.sl
    )

    for chunk in users_chunks:
        for user in chunk:
            send_message_to_user(user, text)


def send_message_to_user(user: User, text: str):
    domain = settings.telegram_bot_api_domain
    token = settings.telegram_bot_api_token

    url = 'https://{domain}/bot{token}/sendMessage'.format(
        domain=domain,
        token=token
    )
    payload = {
        'chat_id': user.telegram_user_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    requests.post(url, payload)
