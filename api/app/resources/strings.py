strings_data = {
    'subscription_purchased': {
        'ўз': 'Табриклаймиз, обуна учун тўлов муваффақиятли амалга оширилди! 🎉 Мана сизнинг Isaev Full Contact гуруҳига эксклюзив киришингиз: {invite_links}. Қўшилинг ва бугун Форехъдаги муваффақият йўлингизни бошланг',
        'uz': "Tabriklaymiz, obuna uchun to'lov muvaffaqiyatli amalga oshirildi! 🎉 Mana sizning Isaev Full Contact guruhiga eksklyuziv kirishingiz: {invite_links}. Qo'shiling va bugun Forex'dagi muvaffaqiyat yo'lingizni boshlang!"
    },
    'invite_group': {
        'ўз': '{name} Гуруҳига Ҳавола',
        'uz': '{name} Guruhiga Havola'
    },
}


def get_string(key: str, language: str | None = None) -> str:
    if language is None:
        language = 'uz'
    if key not in strings_data:
        raise Exception(f'Wrong string key {key}')
    if language not in ['ўз', 'uz']:
        language = 'uz'
    return strings_data[key][language]
