strings_data = {
    'registration_language': {
        'ru': '🇷🇺 Пожалуйста, выберите язык\n\n🇺🇿 Iltimos, tilni tanlang',
        'uz': '🇷🇺 Пожалуйста, выберите язык\n\n🇺🇿 Iltimos, tilni tanlang'
    },
    'registration_language_wrong': {
        'ru': 'Выбран неправильный язык',
        'uz': "Noto'g'ri til tanlangan"
    },
    'registration_name': {
        'ru': 'Привет!!\nПожалуйста, введите своё имя',
        'uz': 'Salom!! Iltimos, ismingizni kiriting'
    },
    'registration_phone': {
        'ru': 'Введите номер телефона или воспользуйтесь кнопкой "Отправить номер"',
        'uz': 'Telefon raqamini kiriting yoki "Raqamni Yuborish" tugmasidan foydalaning'
    },
    'registration_phone_not_verified': {
        'ru': 'Вы ещё не потвердили свой номер телефона. Мы отправили вам смс с кодом, пожалуйста, введите его',
        'uz': 'Siz hali telefon raqamingizni tasdiqlamadingiz. Sizga SMS orqali kod yubordik, iltimos, uni kiriting'
    },
    'registration_phone_user_exists': {
        'ru': 'Пользовтаель с этим номером телефона уже существует',
        'uz': 'Ushbu telefon raqamiga ega foydalanuvchi allaqachon mavjud'
    },
    'registration_phone_otp_sent': {
        'ru': 'Мы отправили вам на номер смс с кодом, пожалуйста, подтвердите свой номер телефона',
        'uz': 'Biz sizning raqamingizga SMS orqali kod yubordik, iltimos, telefon raqamingizni tasdiqlang'
    },
    'registration_phone_otp_wrong_format': {
        'ru': 'Вы отправили неверный формат OTP',
        'uz': "Siz noto'g'ri OTP formatini yubordingiz"
    },
    'registration_phone_otp_wrong': {
        'ru': 'Вы отправили неверный OTP',
        'uz': "Siz noto'g'ri OTP yubordingiz"
    },
    'registration_proactively': {
        'ru': '{name}, вы активировали подписку!',
        'uz': '{name}, siz obunani faollashtirdingiz!'
    },
    'registration_finished': {
        'ru': 'Спасибо, регистрация завершена!',
        'uz': "Rahmat, ro'yxatdan o'tish tugadi!"
    },
    'registration_bonus_activated': {
        'ru': 'Вы активировали бонусную подписку!',
        'uz': 'Siz bonusli obunani faollashtirdingiz!'
    },
    'subscription_menu_message': {
        'ru': 'Для продолжения работы с ботом необходимо приобрести подписку',
        'uz': 'Bot bilan ishlashni davom ettirish uchun siz obunani sotib olishingiz kerak'
    },
    'choose_subscription_text': {
        'ru': 'Выбрать подписку',
        'uz': 'Obunani tanlang'
    },
    'hello_message': {
        'ru': 'Здравствуйте, %s!',
        'uz': 'Salom %s!'
    },
    'send_phone_button_text': {
        'ru': 'Отправить номер',
        'uz': 'Raqamni yuborish'
    },
    'wrong_number_button_text': {
        'ru': 'Неправильный номер',
        'uz': "Noto'g'ri raqam"
    },
    'validation_phone_message': {
        'ru': 'Неправильный формат номер',
        'uz': "Noto'g'ri raqam formati"
    },
    'active_subscription': {
        'ru': 'У вас имеется подписка {name} до {to_date}. Осталось: {days} дней',
        'uz': '{to_date} gacha {name}ga obunangiz bor. Qolgan kun: {days}'
    },

    'subscription_not_found': {
        'ru': 'Такая подписка не найдена',
        'uz': 'Bunday obuna topilmadi'
    },
    'subscription_condition_wrong': {
        'ru': 'Выбрано не праивльное условие подписки',
        'uz': "Noto'g'ri obuna bo’lish sharti tanlangan"
    },
    'back_button': {
        'ru': 'Назад',
        'uz': 'Orqaga'
    },
    'subscription_condition_name': {
        'ru': '%s месяц',
        'uz': '%s oy'
    },
    'subscription_month': {
        'ru': 'месяц',
        'uz': 'oy'
    },
    'provider_provider_not_supported': {
        'ru': 'Выбран провайдер, которого мы не поддерживаем',
        'uz': "Biz qo'llab-quvvatlamaydigan provayder tanlangan"
    },
    'payment_pay_subscription': {
        'ru': 'Оплатить подписку',
        'uz': "Obuna uchun to'lash"
    },
    'payment_subscription_info': {
        'ru': '%s на %d месяцев за $%d',
        'uz': '%s %d oy davomida $%d'
    },
    'payment_cancelation_button': {
        'ru': 'Для отмены нажмите кнопку "Назад"',
        'uz': 'Bekor qilish uchun orqaga tugmasini bosing'
    },
    'subscription_select_condition': {
        'ru': 'Выберите срок подписки',
        'uz': 'Obuna muddatini tanlang'
    },
    'subscription_full_info': {
        'ru': '<b>Подписка:</b> {}\n<b>Срок:</b> {}\n<b>Цена:</b> ${}',
        'uz': '<b>Obuna:</b> {}\n<b>Muddat:</b> {}\n<b>Narx:</b> ${}'
    },
    'subscription_purchased': {
        'ru': 'Подписка куплена!',
        'uz': 'Obuna sotib olindi!'
    },
    'subscription_pay': {
        'ru': '💳 Оплатить',
        'uz': '💳 Оплатить'
    }
}


def get_string(key: str, language: str | None = None):
    if language is None:
        language = 'uz'
    if key not in strings_data:
        raise Exception(f'Wrong string key {key}')
    if language not in ['ru', 'uz']:
        language = 'uz'
    return strings_data[key][language]
