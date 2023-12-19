strings_data = {
    'subscription_purchased': {
        'ru': 'Поздравляем с успешной оплатой подписки! 🎉 Вот ваш эксклюзивный доступ к группе OneZone: {invite_links}. Присоединяйтесь и начните свой путь к успеху на Forex сегодня!',
        'uz': "Tabriklaymiz, obuna uchun to'lov muvaffaqiyatli amalga oshirildi! 🎉 Mana sizning OneZone guruhiga eksklyuziv kirishingiz: {invite_links}. Qo'shiling va bugun Forex'dagi muvaffaqiyat yo'lingizni boshlang!"
    },
    'invite_group': {
        'ru': 'Ссылка на Группу {name}',
        'uz': '{name} Guruhiga Havola'
    }
}


def get_string(key: str, language: str | None = None) -> str:
    if language is None:
        language = 'uz'
    if key not in strings_data:
        raise Exception(f'Wrong string key {key}')
    if language not in ['ru', 'uz']:
        language = 'uz'
    return strings_data[key][language]
