import requests
import logging


def convert_usd_to_uzs(amount: int) -> float:
    url = 'https://api.exchangerate.host/convert'
    params = {
        'from': 'USD',
        'to': 'UZS',
        'amount': amount
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['result']

    logging.error(f"Error while getting exchange course: {response.status_code} - {response.json()}")
    default_course = 10950.0

    return amount * default_course
