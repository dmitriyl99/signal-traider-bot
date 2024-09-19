from typing import List
from datetime import datetime, timedelta

from app.data.models.users import User
from app.helpers import date

import xlsxwriter


def get_users_excel(users: List[User]) -> str:
    workbook = xlsxwriter.Workbook("app/storage/users.xlsx")
    worksheet = workbook.add_worksheet()

    row = 0
    column = 0

    headers = ['ID', 'Telegram ID', 'Имя', 'Номер телефона', "Дата регистрации", "Есть подписка?", "Подписка активна?",
           "Срок подписки, дней", "Дней подписки осталось"]
    for index, header in enumerate(headers):
        worksheet.write(row, column + index, header)
    row += 1
    for user in users:
        worksheet.write(row, column, user.id)
        worksheet.write(row, column + 1, user.telegram_user_id)
        worksheet.write(row, column + 2, user.name)
        worksheet.write(row, column + 3, user.phone)
        worksheet.write(row, column + 4,
                        user.registration_date.strftime('%d.%m.%Y') if user.registration_date else "Не зарегистрирован")
        worksheet.write(row, column + 5, 'Да' if user.subscription else 'Нет')
        worksheet.write(row, column + 6, 'Да' if user.subscription and user.subscription.active else 'Нет')
        worksheet.write(row, column + 7, user.subscription.duration_in_days if user.subscription else '')
        diff_in_days = date.diff_in_days(user.subscription.activation_datetime + timedelta(days=user.subscription.duration_in_days),
                                         datetime.now()) if user.subscription and user.subscription.activation_datetime else ''
        worksheet.write(row, column + 8, diff_in_days)
        row += 1
    workbook.close()

    return workbook.filename
