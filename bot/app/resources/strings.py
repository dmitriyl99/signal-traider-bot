strings_data = {
    'registration_language': {
        'ru': '🇷🇺 Пожалуйста, выберите язык\n\n🇺🇿 Пожалуйста, выберите язык',
        'uz': '🇷🇺 Пожалуйста, выберите язык\n\n🇺🇿 Пожалуйста, выберите язык'
    },
    'registration_name': {
        'ru': 'Привет!!\nПожалуйста, введите своё имя',
        'uz': 'Привет!!\nПожалуйста, введите своё имя'
    },
    'registration_phone': {
        'ru': 'Введите номер телефона или воспользуйтесь кнопкой "Отправить номер"',
        'uz': 'Введите номер телефона или воспользуйтесь кнопкой "Отправить номер"'
    },
    'registration_proactively': {
        'ru': '{name}, вы активировали подписку!',
        'uz': '{name}, вы активировали подписку!'
    },
    'registration_finished': {
        'ru': 'Спасибо, регистрация завершена!',
        'uz': 'Спасибо, регистрация завершена!'
    },
    'subscription_menu_message': {
        'ru': 'Для продолжения работы с ботом необходимо приобрести подписку',
        'uz': 'Для продолжения работы с ботом необходимо приобрести подписку'
    },
    'choose_subscription_text': {
        'ru': 'Выбрать подписку',
        'uz': 'Выбрать подписку'
    },
    'hello_message': {
        'ru': 'Здравствуйте, %s!',
        'uz': 'Здравствуйте, %s!'
    },
    'send_phone_button_text': {
        'ru': 'Отправить номер',
        'uz': 'Отправить номер'
    },
    'wrong_number_button_text': {
        'ru': 'Неправильный номер',
        'uz': 'Неправильный номер'
    },
    'validation_phone_message': {
        'ru': 'Неправильный формат номер',
        'uz': 'Неправильный формат номер'
    },
    'active_subscription': {
        'ru': 'У вас имеется подписка {name} до {to_date}. Осталось: {days} дней',
        'uz': 'У вас имеется подписка {name} до {to_date}. Осталось: {days} дней'
    },
}


def get_string(key: str, language: str | None = None):
    if language is None:
        language = 'uz'
    if key not in strings_data:
        raise Exception(f'Wrong string key {key}')
    if language not in ['ru', 'uz']:
        language = 'uz'
    return strings_data[key][language]
